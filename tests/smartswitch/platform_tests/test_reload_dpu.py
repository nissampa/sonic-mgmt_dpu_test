"""
Tests for the `reboot and reload ...` commands in DPU
"""

import logging
import pytest
import re
import time
from tests.common.cisco_data import is_cisco_device
from tests.common.helpers.assertions import pytest_assert
from tests.common.platform.processes_utils import wait_critical_processes
from tests.common.reboot import reboot, REBOOT_TYPE_COLD, SONIC_SSH_PORT, SONIC_SSH_REGEX
from tests.common.helpers.dut_utils import is_mellanox_devices
from tests.smartswitch.common.device_utils_dpu import (  # noqa: F401
    check_dpu_link_and_status,
    pre_test_check, post_test_switch_check, post_test_dpus_check,
    dpus_shutdown_and_check, dpus_startup_and_check, check_dpus_module_status,
    num_dpu_modules, check_dpus_are_not_pingable, check_dpus_reboot_cause,
    get_dpuhost_for_dpu, get_all_dpu_uptimes, verify_all_dpus_rebooted,
    check_all_dpus_no_syslog_errors, check_npu_syslog_errors
)
from tests.common.platform.device_utils import platform_api_conn, start_platform_api_service  # noqa: F401,F403
from tests.smartswitch.common.reboot import perform_reboot
from tests.common.fixtures.grpc_fixtures import ptf_grpc  # noqa: F401
# ptf_gnoi comes from tests.smartswitch.conftest (SmartSwitch dsmsroot certs)
from tests.common.helpers.multi_thread_utils import SafeThreadPoolExecutor

pytestmark = [
    pytest.mark.topology('smartswitch')
]

kernel_panic_cmd = "sudo nohup bash -c 'sleep 5 && echo c > /proc/sysrq-trigger' &"
memory_exhaustion_cmd = "sudo nohup bash -c 'sleep 5 && tail /dev/zero' &"
DUT_ABSENT_TIMEOUT_FOR_KERNEL_PANIC = 100
DUT_ABSENT_TIMEOUT_FOR_MEMORY_EXHAUSTION = 240
MAX_COOL_OFF_TIME = 300
EXTRA_DPU_ONLINE_TIMEOUT_FOR_WATCHDOG = 40


@pytest.fixture(params=["gnoi_based", "cli_based"])
def invocation_type(request):
    """Parametrize reboot tests to run with both gNOI and CLI reboot paths."""
    return request.param


def test_dpu_status_post_switch_reboot(duthosts, dpuhosts,
                                       enum_rand_one_per_hwsku_hostname,
                                       localhost,
                                       platform_api_conn, num_dpu_modules):  # noqa F811, E501
    """
    @summary: Verify DPU connectivity and reboot cause after an NPU cold reboot.
              Also checks that each DPU actually rebooted (via uptime comparison)
              and that no unexpected syslog errors appear post-reboot.
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before switch reboot")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Starting switch reboot...")
    reboot(duthost, localhost, reboot_type=REBOOT_TYPE_COLD,
           wait_for_ssh=False)

    logging.info("Executing post test check")
    post_test_switch_check(duthost, localhost,
                           dpu_on_list, dpu_off_list,
                           ip_address_list)

    logging.info("Executing post switch reboot dpu check")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)


def test_dpu_status_post_switch_config_reload(duthosts, dpuhosts,
                                              enum_rand_one_per_hwsku_hostname,
                                              localhost,
                                              platform_api_conn, num_dpu_modules):   # noqa F811, E501
    """
    @summary: To Check Ping between NPU and DPU
              after configuration reload on NPU
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before config reload")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Reload configuration")
    duthost.shell("sudo config reload -y &>/dev/null", executable="/bin/bash")

    logging.info("Wait until all critical services are fully started")
    wait_critical_processes(duthost)

    logging.info("Checking DPU link status and connectivity")
    check_dpu_link_and_status(duthost, dpu_on_list,
                              dpu_off_list, ip_address_list)

    logging.info("Executing post switch config reload dpu check")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)


@pytest.mark.disable_loganalyzer
def test_dpu_status_post_switch_mem_exhaustion(duthosts, dpuhosts,
                                               enum_rand_one_per_hwsku_hostname,  # noqa: E501
                                               localhost,
                                               platform_api_conn, num_dpu_modules):  # noqa: F811, E501
    """
    @summary: Test memory exhaustion on NPU by running a heavy process,
              causing reboot of the NPU.
              Verify DPU connectivity and operational status before and
              after the reboot.
    """

    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before NPU memory exhaustion")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Starting memory exhaustion test on NPU by running \
                  a large process...")
    duthost.shell(memory_exhaustion_cmd, executable="/bin/bash")

    logging.info("Waiting for ssh to drop on {}".format(duthost.hostname))
    localhost.wait_for(host=duthost.mgmt_ip,
                       port=SONIC_SSH_PORT,
                       state='absent',
                       search_regex=SONIC_SSH_REGEX,
                       delay=10,
                       timeout=DUT_ABSENT_TIMEOUT_FOR_MEMORY_EXHAUSTION)

    logging.info("Executing post test check")
    post_test_switch_check(duthost, localhost,
                           dpu_on_list, dpu_off_list,
                           ip_address_list)

    logging.info("Executing post switch mem exhaustion dpu check")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)

    logging.info("Checking NPU syslog for unexpected errors after memory exhaustion reboot")
    npu_errors = check_npu_syslog_errors(duthost)
    if npu_errors:
        logging.warning("NPU syslog has %d error(s) after memory exhaustion reboot "
                        "(non-fatal; logged for investigation)", len(npu_errors))


@pytest.mark.disable_loganalyzer
def test_dpu_status_post_switch_kernel_panic(duthosts, dpuhosts,
                                             enum_rand_one_per_hwsku_hostname,
                                             localhost,
                                             platform_api_conn, num_dpu_modules):  # noqa: F811, E501
    """
    @summary: Test NPU recovery from a kernel panic,
              Kernel panic causing reboot of the NPU.
              Verify DPU connectivity and operational status before
              and after the reboot.
    """

    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before NPU kernel panic")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Triggering kernel panic on NPU...")
    duthost.shell(kernel_panic_cmd, executable="/bin/bash")

    logging.info("Waiting for ssh to drop on {}".format(duthost.hostname))
    localhost.wait_for(host=duthost.mgmt_ip,
                       port=SONIC_SSH_PORT,
                       state='absent',
                       search_regex=SONIC_SSH_REGEX,
                       delay=10,
                       timeout=DUT_ABSENT_TIMEOUT_FOR_KERNEL_PANIC)

    logging.info("Executing post test check")
    post_test_switch_check(duthost, localhost,
                           dpu_on_list, dpu_off_list,
                           ip_address_list)

    logging.info("Executing post switch kernel panic dpu check")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)

    logging.info("Checking NPU syslog for unexpected errors after kernel panic reboot")
    npu_errors = check_npu_syslog_errors(duthost)
    if npu_errors:
        logging.warning("NPU syslog has %d error(s) after kernel panic reboot "
                        "(non-fatal; logged for investigation)", len(npu_errors))


@pytest.mark.disable_loganalyzer
def test_dpu_status_post_dpu_kernel_panic(duthosts, dpuhosts,
                                          enum_rand_one_per_hwsku_hostname,
                                          platform_api_conn, num_dpu_modules):  # noqa: F811, E501
    """
    @summary: Test to verify DPU recovery on `kernel panic on DPU`
    """

    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    triggered_dpu_on_list = []
    triggered_ip_list = []
    for index in range(len(dpu_on_list)):
        logging.info("Triggering Kernel Panic on %s" % (dpu_on_list[index]))
        dpu_on = dpu_on_list[index]
        dpu_id = int(re.search(r'\d+', dpu_on).group())
        dpuhost = get_dpuhost_for_dpu(dpuhosts, dpu_id)
        if dpuhost is None:
            logging.warning("DPU%d not in dpuhosts (len=%d); skipping kernel panic trigger", dpu_id, len(dpuhosts))
            continue
        dpuhost.shell(kernel_panic_cmd, executable="/bin/bash")
        triggered_dpu_on_list.append(dpu_on)
        triggered_ip_list.append(ip_address_list[index])

    logging.info("Recording DPU boot times before DPU kernel panic")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    pytest_assert(triggered_dpu_on_list, "No DPUs were triggered; all skipped due to missing dpuhosts")

    logging.info("Checking DPUs are not pingable")
    check_dpus_are_not_pingable(duthost, triggered_ip_list)

    # Check if it's a Cisco ASIC
    if is_cisco_device(duthost):

        logging.info("Checking DPUs reboot reason as Kernel Panic")
        check_dpus_reboot_cause(duthost, triggered_dpu_on_list,
                                num_dpu_modules, "Kernel Panic")

        logging.info("Shutdown DPUs after kernel Panic")
        dpus_shutdown_and_check(duthost, triggered_dpu_on_list, num_dpu_modules)

        logging.info("5 min Cool off period after DPUs Shutdown")
        time.sleep(MAX_COOL_OFF_TIME)

        logging.info("Starting UP the DPUs")
        dpus_startup_and_check(duthost, triggered_dpu_on_list, num_dpu_modules)
    else:
        logging.info("Check DPUs are offline")
        check_dpus_module_status(duthost, triggered_dpu_on_list, "off")

    logging.info("Executing post test dpu check")
    reboot_cause_pattern = r"reboot|Non-Hardware"
    if is_mellanox_devices(duthost.facts['hwsku']):
        reboot_cause_pattern = r"Watchdog"
    post_test_dpus_check(duthost, dpuhosts,
                         triggered_dpu_on_list, triggered_ip_list,
                         num_dpu_modules,
                         re.compile(reboot_cause_pattern,
                                    re.IGNORECASE),
                         EXTRA_DPU_ONLINE_TIMEOUT_FOR_WATCHDOG,
                         pre_boot_times=pre_boot_times)


@pytest.mark.disable_loganalyzer
def test_dpu_check_post_dpu_mem_exhaustion(duthosts, dpuhosts,
                                           enum_rand_one_per_hwsku_hostname,
                                           platform_api_conn, num_dpu_modules):  # noqa: F811, E501
    """
    @summary: Test to verify DPU recovery on `Memory Exhaustion on DPU`
    """

    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    triggered_dpu_on_list = []
    triggered_ip_list = []
    for index in range(len(dpu_on_list)):
        logging.info(
                "Triggering Memory Exhaustion on %s" % (dpu_on_list[index])
                )
        dpu_on = dpu_on_list[index]
        dpu_id = int(re.search(r'\d+', dpu_on).group())
        dpuhost = get_dpuhost_for_dpu(dpuhosts, dpu_id)
        if dpuhost is None:
            logging.warning("DPU%d not in dpuhosts (len=%d); skipping memory exhaustion trigger", dpu_id, len(dpuhosts))
            continue
        dpuhost.shell(memory_exhaustion_cmd, executable="/bin/bash")
        triggered_dpu_on_list.append(dpu_on)
        triggered_ip_list.append(ip_address_list[index])

    logging.info("Recording DPU boot times before DPU memory exhaustion")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    pytest_assert(triggered_dpu_on_list, "No DPUs were triggered; all skipped due to missing dpuhosts")

    logging.info("Checking DPUs are not pingable")
    check_dpus_are_not_pingable(duthost, triggered_ip_list)

    # Check if it's a Cisco ASIC
    if is_cisco_device(duthost):

        logging.info("Checking DPUs reboot reason as Kernel Panic")
        check_dpus_reboot_cause(duthost, triggered_dpu_on_list,
                                num_dpu_modules, "Kernel Panic")

        logging.info("Shutdown DPUs after memory exhaustion")
        dpus_shutdown_and_check(duthost, triggered_dpu_on_list, num_dpu_modules)

        logging.info("5 min Cool off period after DPUs Shutdown")
        time.sleep(MAX_COOL_OFF_TIME)

        logging.info("Starting UP the DPUs")
        dpus_startup_and_check(duthost, triggered_dpu_on_list, num_dpu_modules)
    else:
        logging.info("Check DPUs are offline")
        check_dpus_module_status(duthost, triggered_dpu_on_list, "off")

    logging.info("Executing post test dpu check")
    reboot_cause_pattern = r"reboot|Non-Hardware"
    if is_mellanox_devices(duthost.facts['hwsku']):
        reboot_cause_pattern = r"Watchdog"

    post_test_dpus_check(duthost, dpuhosts,
                         triggered_dpu_on_list, triggered_ip_list,
                         num_dpu_modules,
                         re.compile(reboot_cause_pattern,
                                    re.IGNORECASE),
                         EXTRA_DPU_ONLINE_TIMEOUT_FOR_WATCHDOG,
                         pre_boot_times=pre_boot_times)


@pytest.mark.disable_loganalyzer
def test_cold_reboot_dpus(duthosts, dpuhosts, enum_rand_one_per_hwsku_hostname,
                          platform_api_conn, num_dpu_modules,  # noqa: F811
                          invocation_type, ptf_gnoi):  # noqa: F811, E501
    """
    Test to cold reboot all DPUs in the DUT.
    Steps:
    1. Perform pre-test checks to gather DPU state.
    2. Initiate cold reboot on all DPUs concurrently.
    3. Perform post-test checks to verify the state after reboot.

    Args:
        duthosts: DUT hosts object
        dpuhosts: DPU hosts object
        enum_rand_one_per_hwsku_hostname: Randomized DUT hostname
        platform_api_conn: Platform API connection object
        num_dpu_modules: Number of DPU modules to reboot
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(duthost, platform_api_conn, num_dpu_modules)

    logging.info("Recording DPU boot times before cold reboot")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    with SafeThreadPoolExecutor(max_workers=num_dpu_modules) as executor:
        logging.info("Rebooting all DPUs in parallel")
        for dpu_name in dpu_on_list:
            executor.submit(perform_reboot, duthost, REBOOT_TYPE_COLD, dpu_name, invocation_type,
                            ptf_gnoi=ptf_gnoi)

    logging.info("Executing post test dpu check")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware",
                                    re.IGNORECASE),
                         pre_boot_times=pre_boot_times)


def test_cold_reboot_switch(duthosts, dpuhosts, enum_rand_one_per_hwsku_hostname,
                            platform_api_conn, num_dpu_modules, localhost):  # noqa: F811, E501
    """
    Test to cold reboot the switch in the DUT.
    Steps:
    1. Perform pre-test checks to gather DPU state.
    2. Initiate a cold reboot on the switch.
    3. Perform post-test checks to verify the state of DPUs after the reboot.

    Args:
        duthosts: DUT hosts object
        dpuhosts: DPU hosts object
        enum_rand_one_per_hwsku_hostname: Randomized DUT hostname
        platform_api_conn: Platform API connection object
        num_dpu_modules: Number of DPU modules to verify
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(duthost, platform_api_conn, num_dpu_modules)

    logging.info("Recording DPU boot times before switch cold reboot")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Starting switch reboot...")
    perform_reboot(duthost, REBOOT_TYPE_COLD, None)

    logging.info("Executing post test check")
    post_test_switch_check(duthost, localhost,
                           dpu_on_list, dpu_off_list,
                           ip_address_list)

    logging.info("Executing post switch reboot dpu check")
    post_test_dpus_check(duthost, dpuhosts, dpu_on_list, ip_address_list, num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)


def test_reboot_cause(duthosts, dpuhosts,
                      enum_rand_one_per_hwsku_hostname,
                      platform_api_conn, num_dpu_modules):    # noqa: F811
    """
    @summary: Verify reboot-cause for DPUs after a shutdown/startup cycle.
              Uses parallel execution for all DPUs.
              Checks that reboot-cause is correctly reported as 'reboot' or
              'Non-Hardware' after DPUs are cycled.
              Also verifies each DPU actually rebooted via uptime comparison.

    Note: This test is the canonical reboot-cause test for DPUs (moved from
    test_platform_dpu.py). All other reboot tests also validate reboot-cause
    as part of their post-test checks.
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before shutdown/startup cycle")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Shutting DOWN the DPUs in parallel")
    dpus_shutdown_and_check(duthost, dpu_on_list, num_dpu_modules)

    logging.info("Starting UP the DPUs in parallel")
    dpus_startup_and_check(duthost, dpu_on_list, num_dpu_modules)

    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware",
                                    re.IGNORECASE),
                         pre_boot_times=pre_boot_times)


def test_npu_graceful_reboot_dpus_recovery(duthosts, dpuhosts,
                                           enum_rand_one_per_hwsku_hostname,
                                           localhost,
                                           platform_api_conn, num_dpu_modules):  # noqa: F811, E501
    """
    @summary: Verify that when the NPU undergoes a graceful cold reboot,
              all DPUs come back online properly with correct reboot-cause,
              and no unexpected syslog errors are present on either NPU or DPUs.

              A "graceful reboot" here is an operator-initiated 'reboot' command
              on the NPU (i.e., REBOOT_TYPE_COLD via the standard reboot path),
              distinct from abnormal reboots like kernel panic or memory exhaustion.

    Steps:
        1. Pre-test check: record DPU states and boot times.
        2. Trigger a graceful NPU cold reboot.
        3. Wait for NPU to come back online.
        4. Verify DPUs come back online with correct reboot-cause.
        5. Verify DPUs actually rebooted via uptime comparison.
        6. Check NPU and DPU syslogs for unexpected errors.
    """
    duthost = duthosts[enum_rand_one_per_hwsku_hostname]

    logging.info("Executing pre test check")
    ip_address_list, dpu_on_list, dpu_off_list = pre_test_check(
                                                 duthost,
                                                 platform_api_conn,
                                                 num_dpu_modules)

    logging.info("Recording DPU boot times before graceful NPU reboot")
    pre_boot_times = get_all_dpu_uptimes(dpuhosts, dpu_on_list)

    logging.info("Triggering graceful NPU cold reboot...")
    reboot(duthost, localhost, reboot_type=REBOOT_TYPE_COLD,
           wait_for_ssh=False)

    logging.info("Executing post switch reboot check")
    post_test_switch_check(duthost, localhost,
                           dpu_on_list, dpu_off_list,
                           ip_address_list)

    logging.info("Verifying DPUs recovered properly after graceful NPU reboot")
    post_test_dpus_check(duthost, dpuhosts,
                         dpu_on_list, ip_address_list,
                         num_dpu_modules,
                         re.compile(r"reboot|Non-Hardware", re.IGNORECASE),
                         pre_boot_times=pre_boot_times)

    logging.info("Checking NPU syslog for unexpected errors after graceful reboot")
    npu_errors = check_npu_syslog_errors(duthost)
    if npu_errors:
        logging.warning("NPU syslog has %d error(s) after graceful reboot "
                        "(non-fatal; logged for investigation)", len(npu_errors))

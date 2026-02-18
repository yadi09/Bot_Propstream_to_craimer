from bot.logger import setup_logger
from bot.propstream_client import fetch_properties
from bot.crm_client import send_to_crm
from bot.tenants import get_enabled_tenants

logger = setup_logger()


def run_tenant(tenant):
    tenant_name = tenant.get("name", tenant.get("id", "unknown"))
    logger.info(f"--> Starting tenant job: {tenant_name}")

    data = fetch_properties(tenant)
    if not data:
        logger.warning(f"No data fetched for tenant: {tenant_name}. Retrying once...")
        data = fetch_properties(tenant)

    if not data:
        logger.error(f"Failed to fetch data for tenant: {tenant_name}")
        return

    properties = data.get("properties", [])
    logger.info(f"Fetched {len(properties)} properties for tenant: {tenant_name}")
    send_to_crm(data, tenant)


def run_all_enabled_tenants():
    tenants = get_enabled_tenants()
    if not tenants:
        logger.warning("No enabled tenants to process.")
        return

    for tenant in tenants:
        run_tenant(tenant)

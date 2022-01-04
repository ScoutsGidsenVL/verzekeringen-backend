import logging

from scouts_insurances.insurances.utils import InsuranceSettingsHelper

from scouts_auth.inuits.utils import SettingsHelper


logger = logging.getLogger(__name__)


class EmailSettingsUtil(SettingsHelper):
    @staticmethod
    def is_send_in_blue() -> bool:
        return EmailSettingsUtil.get_bool("USE_SEND_IN_BLUE") and EmailSettingsUtil.get("EMAIL_BACKEND")

    @staticmethod
    def log_email_settings():

        insurance_requester_address = "[ REQUESTER EMAIL ADDRESS ]"
        insurer_address = EmailSettingsUtil.get("EMAIL_INSURER_ADDRESS", " !! NOT SET !!")
        victim_address = "[ VICTIM EMAIL ADDRESS ]"
        declarant_address = "[ DECLARANT EMAIL ADDRESS ]"
        if InsuranceSettingsHelper.is_test():
            if InsuranceSettingsHelper.is_acceptance():
                insurer_address = "[ DECLARANT EMAIL ADDRESS ]"
                victim_address = declarant_address
            else:
                insurance_requester_address = (
                    "[ setting: EMAIL_INSURANCE_REQUESTER_ADDRESS_DEBUG ] ("
                    + EmailSettingsUtil.get("EMAIL_INSURANCE_REQUESTER_ADDRESS_DEBUG", " !! NOT SET !!")
                    + ")"
                )
                insurer_address = (
                    "[ setting: EMAIL_INSURER_ADDRESS_DEBUG ] ("
                    + EmailSettingsUtil.get("EMAIL_INSURER_ADDRESS_DEBUG", " !! NOT SET !!")
                    + ")"
                )
                victim_address = (
                    "[ setting: EMAIL_VICTIM_ADDRESS_DEBUG ] ("
                    + EmailSettingsUtil.get("EMAIL_VICTIM_ADDRESS_DEBUG", " !! NOT SET !!")
                    + ")"
                )
                declarant_address = (
                    "[ setting: EMAIL_DECLARANT_ADDRESS_DEBUG [ ("
                    + EmailSettingsUtil.get("EMAIL_DECLARANT_ADDRESS_DEBUG", " !! NOT SET !!")
                    + ")"
                )

        logger.debug(
            "======================================================================================================"
        )
        logger.debug("EMAIL SETTINGS")
        logger.debug(
            "======================================================================================================"
        )
        logger.debug("Mail will be sent with %s", EmailSettingsUtil.get("EMAIL_BACKEND"))
        logger.debug(
            "======================================================================================================"
        )
        logger.debug("%s:", InsuranceSettingsHelper.__class__.__name__)
        logger.debug("is_test()                                            : %s", InsuranceSettingsHelper.is_test())
        logger.debug(
            "is_acceptance()                                      : %s", InsuranceSettingsHelper.is_acceptance()
        )
        logger.debug("INSURANCES: Insurance requester mails will be sent to: %s", insurance_requester_address)
        logger.debug("CLAIMS: Insurer mails will be sent to                : %s", insurer_address)
        logger.debug("CLAIMS: Victim emails will be sent to                : %s", victim_address)
        logger.debug("CLAIMS: Declarant emails will be sent to             : %s", declarant_address)
        logger.debug(
            "======================================================================================================"
        )
        logger.debug("DEBUG                      : %s", EmailSettingsUtil.get_bool("DEBUG", False, "- NOT SET -"))
        logger.debug(
            "IS_ACCEPTANCE              : %s", EmailSettingsUtil.get_bool("IS_ACCEPTANCE", False, "- NOT SET -")
        )
        logger.debug("EMAIL_DEBUG_RECIPIENT      : %s", EmailSettingsUtil.get("EMAIL_DEBUG_RECIPIENT", "- NOT SET -"))
        logger.debug("EMAIL_BACKEND              : %s", EmailSettingsUtil.get("EMAIL_BACKEND", "- NOT SET -"))
        logger.debug("ANYMAIL                    : %s", EmailSettingsUtil.get("ANYMAIL", "- NOT SET -"))
        logger.debug("EMAIL_INSURANCE_FROM       : %s", EmailSettingsUtil.get("EMAIL_INSURANCE_FROM", "- NOT SET -"))
        logger.debug("EMAIL_INSURANCE_CC         : %s", EmailSettingsUtil.get("EMAIL_INSURANCE_CC", "- NOT SET -"))
        logger.debug("EMAIL_INSURANCE_BCC        : %s", EmailSettingsUtil.get("EMAIL_INSURANCE_BCC", "- NOT SET -"))
        logger.debug("EMAIL_TEMPLATE             : %s", EmailSettingsUtil.get("EMAIL_TEMPLATE", "- NOT SET -"))
        logger.debug("EMAIL_INSURER_ADDRESS      : %s", EmailSettingsUtil.get("EMAIL_INSURER_ADDRESS", "- NOT SET -"))
        logger.debug(
            "EMAIL_INSURER_ADDRESS_DEBUG: %s", EmailSettingsUtil.get("EMAIL_INSURER_ADDRESS_DEBUG", "- NOT SET -")
        )
        logger.debug("EMAIL_URL                  : %s", EmailSettingsUtil.get("EMAIL_URL", "- NOT SET -"))
        logger.debug("EMAIL_SENDER               : %s", EmailSettingsUtil.get("EMAIL_SENDER", "- NOT SET -"))
        logger.debug("EMAIL_RECIPIENTS           : %s", EmailSettingsUtil.get("EMAIL_RECIPIENTS", "- NOT SET -"))
        logger.debug("EMAIL_HOST                 : %s", EmailSettingsUtil.get("EMAIL_HOST", "- NOT SET -"))
        logger.debug("EMAIL_PORT                 : %s", EmailSettingsUtil.get("EMAIL_PORT", "- NOT SET -"))
        logger.debug(
            "USE_SEND_IN_BLUE           : %s", EmailSettingsUtil.get_bool("USE_SEND_IN_BLUE", False, "- NOT SET -")
        )
        logger.debug(
            "======================================================================================================"
        )

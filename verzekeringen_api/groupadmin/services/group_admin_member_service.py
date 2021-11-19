import logging
from typing import List
from datetime import date, datetime, timedelta

from django.conf import settings

from groupadmin.models import ScoutsMember, ScoutsMemberSearchMember, ScoutsMemberSearchResponse
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberService(GroupAdmin):
    def search_member_filtered(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str,
        group: str = None,
        include_inactive: bool = False,
    ) -> List[ScoutsMemberSearchMember]:
        response: ScoutsMemberSearchResponse = self.search_member(active_user, term)

        if group:
            return self.search_member_filtered_by_group(active_user, response, group, include_inactive)
        else:
            return self.search_member_filtered_by_activity(active_user, response, include_inactive)

        if group:
            return self._parse_search_results_for_group(active_user, json, group, include_inactive=include_inactive)
        else:
            return self._parse_search_results(active_user, json, include_inactive=include_inactive)

    def search_member_filtered_by_group(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: ScoutsMemberSearchResponse,
        group: str,
        include_inactive: bool = False,
    ) -> List[ScoutsMemberSearchMember]:
        results = []
        for partial_member in response.members:
            member: ScoutsMember = self.get_member_info(active_user, partial_member.group_admin_id)

            for function in member.functions:
                if function.group == group:
                    results.append(member)

        return [member.to_search_member() for member in results]

    def search_member_filtered_by_activity(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: ScoutsMemberSearchResponse,
        include_inactive: bool = False,
    ) -> List[ScoutsMemberSearchMember]:
        results = []
        # The "activity epoch" after which a member is deemed a past active member
        activity_epoch = self._calculate_activity_epoch(datetime.now(), 3)

        for partial_member in response.members:
            member: ScoutsMember = self.get_member_info(active_user, partial_member.group_admin_id)

            was_active = False
            end_of_activity_period_counter = 0
            for function in member.functions:
                # Member was active in at least one function since the activity epoch, don't look further
                if was_active:
                    break

                end_of_activity_period: datetime = function.end

                # Member has ended an activity for at least one function, examine
                if end_of_activity_period:
                    # An end date of a function was registered in the member record
                    end_of_activity_period_counter = end_of_activity_period_counter + 1
                    from inuits.utils import DateUtils

                    logger.debug("DATE: %s", isinstance(end_of_activity_period, date))
                    logger.debug("DATETIME: %s", isinstance(end_of_activity_period, datetime))

                    # end_of_activity_period = DateUtils.datetime_from_isoformat(end_of_activity_period).date()
                    end_of_activity_period = end_of_activity_period.date()

                    # Was the end date of the activity after the activity epoch ?
                    if activity_epoch < end_of_activity_period:
                        # Not all insurance types require recently active members to be included in the search results
                        # (currently only temporary insurance for non-members)
                        was_active = True

                        if include_inactive:
                            results.append(member)

            # The member is still active
            if end_of_activity_period_counter == 0:
                results.append(member)

        return [member.to_search_member() for member in results]

    def _calculate_activity_epoch(self, current_date: date, number_of_years: int) -> date:
        return (current_date - timedelta(days=number_of_years * 365)).date()

#!  /usr/bin/env python

from typing import Tuple

Fish = Tuple[int, int] # type: Fish type -> [campaignID, fishNumberInCampaign] (fishNumberInCampaign = Nth fish in the json file)
FishName = Tuple[int, str] # type: FishName -> [campaignID, fishName] (fishName = "id" field in jsons)


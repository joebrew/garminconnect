#!/usr/bin/env python3
import yaml
credentials = yaml.load(open('credentials.yaml'))

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date
import datetime
import pandas as pd

"""
Enable debug logging
"""
#import logging
#logging.basicConfig(level=logging.DEBUG)

today = date.today()


"""
Initialize Garmin client with credentials
Only needed when your program is initialized
"""
try:
    client = Garmin(credentials['email'], credentials['password'])
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()


"""
Login to Garmin Connect portal
Only needed at start of your program
The library will try to relogin when session expires
"""
try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client login")
    quit()


"""
Get full name from profile
"""
try:
    print(client.get_full_name())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get full name")
    quit()


"""
Get unit system from profile
"""
try:
    print(client.get_unit_system())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get unit system: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get unit system")
    quit()

"""
Joe's function for getting steps data
"""
def get_steps(date):
    try:
        return(client.get_steps_data(date))
    except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occurred during Garmin Connect Client get heart rates: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occurred during Garmin Connect Client get steps data")
        quit()

# List through dates
date_list = pd.date_range(start="2020-07-01",end=today.isoformat()).strftime('%Y-%m-%d')
out_list = []
for i in range(len(date_list)):
    this_date = date_list[i]
    steps = get_steps(this_date)
    df = pd.DataFrame(steps)
    n_steps = df['steps'].sum()
    out_df = pd.DataFrame({'date': [this_date], 'steps': [n_steps]})
    out_list.append(out_df)
df = pd.concat(out_list)

"""
Get steps data
"""

try:
    print(client.get_steps_data(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get heart rates: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get steps data")
    quit()



"""
Get activity data
"""
try:
    print(client.get_stats(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats")
    quit()


"""
Get heart rate data
"""
try:
    print(client.get_heart_rates(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get heart rates: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get heart rates")
    quit()


"""
Get body composition data
"""
try:
    print(client.get_body_composition(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get body composition")
    quit()


"""
Get stats and body composition data
"""
try:
    print(client.get_stats_and_body(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats and body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats and body composition")
    quit()


"""
Get activities data
"""
try:
    activities = client.get_activities(0,1) # 0=start, 1=limit
    print(activities)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activities: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activities")
    quit()

"""
Download an Activity
"""

try:
  for activity in activities:
      activity_id = activity["activityId"]

      gpx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
      output_file = f"./{str(activity_id)}.gpx"
      with open(output_file, "wb") as fb:
          fb.write(gpx_data)

      tcx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
      output_file = f"./{str(activity_id)}.tcx"
      with open(output_file, "wb") as fb:
          fb.write(tcx_data)

      zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
      output_file = f"./{str(activity_id)}.zip"
      with open(output_file, "wb") as fb:
          fb.write(zip_data)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activity data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activity data")
    quit()

"""
Get sleep data
"""
try:
    print(client.get_sleep_data(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get sleep data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get sleep data")
    quit()
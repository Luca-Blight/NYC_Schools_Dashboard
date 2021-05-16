from sodapy import Socrata

class Client:
    APP_TOKEN = "XNKZJVsscuBPRteOXyyM6G3yc"
    ROOT_URL = "data.cityofnewyork.us"
    # END_POINT_ONE - School_Location Dataset
    END_POINT_ONE = "ahjc-fdu3" 
    # END_POINT_TWO - Attendance_Pop Dataset
    END_POINT_TWO = "ewhs-k7um"
    
    def request_school_locs(self):
        client = Socrata(self.ROOT_URL, app_token = self.APP_TOKEN)
        data = client.get(self.END_POINT_ONE, content_type = "json")
        return data    
    def request_attendance_pop(self):
        client = Socrata(self.ROOT_URL, app_token = self.APP_TOKEN)
        data = client.get(self.END_POINT_TWO, content_type = "json")
        return data

school_loc_details = Client().request_school_locs()
attn_pop_details = Client().request_attendance_pop()

# old_results = pd.read_csv('2017 School_Results.csv').fillna(0)
# new_results = old_results.to_dict(orient='records')
# result_details = [results for results in new_results]
# print(result_details)
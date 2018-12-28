import csv
import json 
import requests


class GeoNames(object):
    # use these class variables for demo purposes
    url = 'http://api.geonames.org'
    endpoint = '/findNearbyPostalCodesJSON'
 
    def __init__(self, name=None):
        self.lookup_name = name

    def get_lookup_name(self):
        if self.lookup_name:
            return self.lookup_name
        else:
            raise AttributeError('A lookup name for this object was not provided. Use "name" argument when initializing.')

    def set_params(self):
        key_names = input('Provide parameter names (separated by spaces): ').split()
        params = {} 
        for k in key_names:
            value = input('Type the value desired for  "' + k + '": ')
            if k in ['lat','lng']:
                value = int(value)
            params.update({k: value})
        self.params = params

    def get_data(self, to_csv=False):
        try:
            resp = requests.get(GeoNames.url + GeoNames.endpoint, params=self.params)
        except AttributeError as e:
            print(str(e) + '.', 'Call set_params() before getting data.')
        except:
            print('Something went wrong with the request.')
        else:
            data = json.loads(resp.text)
            if to_csv:
                with open('geonames_output.csv', 'w') as f:
                    top_level = 'postalCodes' # depends on endpoint
                    headers = list(data[top_level][0].keys())
                    f_csv = csv.DictWriter(f, fieldnames=headers)
                    f_csv.writeheader()
                    f_csv.writerows(data[top_level])
                return 'Data written to CSV file: ./geonames_output.csv'
            else:
                return data




if __name__ == '__main__':
    gn = GeoNames(name='first_lookup')
    print(gn.get_lookup_name()) 
    gn.set_params()
    print(gn.get_data(to_csv=True)) 

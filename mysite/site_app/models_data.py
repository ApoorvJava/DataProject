import os
import logging as logger
from .models import Weather,Yield,Results

logger.basicConfig(filename="log.txt")

def WeatherData():

    ######################################
    #Mention the path of all weather files
    ######################################
    path = 'C:/Users/dell/Desktop/java/code-challenge-template/wx_data/'
    files = os.listdir(path)
    
    #############################
    #Iterating over all the files
    #############################
    all_objects = []
    for file_name in files:
        file_path = os.path.join(path,file_name)

        with open(file_path) as f:
            all_data = f.readlines()
        
        station_id = file_name.split('.')[0]

        for data in all_data:
            
            try:
                data = data.replace('\n','').split('\t')
                date = data[0][0:4] + '-' + data[0][4:6] + '-'+ data[0][6:8]
                    
                a = Weather(date=date, max_temperature=float(data[1])/10, min_temperature=float(data[2])/10, precipitation=float(data[3])/10, station_id=station_id)
                
            except ValueError:
                logger.warning(f'Value of one of the objects is not correct')
            except Exception as e:
                logger.warning(f'Skipping as getting error {e}')
                continue

            count = 0
            ####################################################
            #Iterating over all the objects for duplicates check
            ####################################################
            for i in Weather.objects.all():
                if a.id != i.id and a.date == str(i.date) and i.max_temperature==a.max_temperature and i.min_temperature==a.min_temperature and i.precipitation==a.precipitation and i.station_id==a.station_id:
                    count +=1
                    break

            if count == 0:
                all_objects.append(a)

    Weather.objects.bulk_create(all_objects)


def YieldData():

    ######################################
    #Mention the path of all Yield files
    ######################################
    path = 'C:/Users/dell/Desktop/java/code-challenge-template/yld_data/'
    files = os.listdir(path)
    all_objects = []
    #############################
    #Iterating over all the files
    #############################
    for file_name in files:
        file_path = os.path.join(path,file_name)

        with open(file_path) as f:
            all_data = f.readlines()
        
        station_id = file_name.split('.')[0]

        for data in all_data:
            data = data.replace('\n','').split('\t')
            a = Yield(total_corn = int(data[0]), year= int(data[1]))
            
            if len(Yield.objects.all()) == 0:
                a.save()

            count = 0
            ####################################################
            #Iterating over all the objects for duplicates check
            ####################################################
            for i in Yield.objects.all():
                if i.total_corn == a.total_corn and i.year == a.year:
                    count +=1
                    break

            if count == 0:
                all_objects.append(a)

    Yield.objects.bulk_create(all_objects)


def ResultsData():
    all_values = Weather.objects.all().values()

    years = []
    stations = []
    for date in all_values:
        year = str(date['date']).split('-')[0]
        station = date['station_id']
        years.append(year)
        stations.append(station)
    years = set(years)
    stations = set(stations)

    all_objects = []
    all_data = []
    for y in years:
        for s in stations:
            if Results.objects.filter(year= y).filter(station_id= s).exists():
                continue

            data = Weather.objects.filter(date__year=y).filter(station_id=s).only('max_temperature', 'min_temperature', 'precipitation').values()
            length = len(data)
            if length == 0:
                continue
                
            avg_max_temperature = 0
            avg_min_temperature = 0
            total_precipitation = 0

            for d in data:
                avg_max_temperature += d['max_temperature']
                avg_min_temperature += d['min_temperature']
                total_precipitation += d['precipitation']
        
            avg_max_temperature = avg_max_temperature/length
            avg_min_temperature = avg_min_temperature/length
            total_precipitation = total_precipitation/100
            station_id = s
            year = y
           
            result = Results(year = int(year), avg_max_temperature = avg_max_temperature, avg_min_temperature=avg_min_temperature, total_precipitation= total_precipitation,station_id = station_id)
            all_objects.append(result)
            
    Results.objects.bulk_create(all_objects)
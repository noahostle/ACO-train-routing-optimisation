from multi import run
import time
import subprocess 


print()
TRIALS = 20
MAX_STATIONS = 10
STEP = 1

#set to false if you dont want to use custom list
CUSTOM_SIZES = True
CUSTOM_SIZES_LIST = [

	#5,10,15,20,25,30,35,40,45,50,60,70,80,90,100,
	125,150,175,200

]

stations_arr=[]
if CUSTOM_SIZES:
	stations_arr = CUSTOM_SIZES_LIST
else:
	stations_arr = range(1,MAX_STATIONS+1,STEP)


average_times={}

i=0
l=len(stations_arr)
for s in stations_arr:
	print(f"[+]	Processed station 	{i} / {l}", end="\r")
	i+=1
	avgtime=0

	for t in range(0,TRIALS):
		start=time.time()
		run(s)
		end=time.time()
		avgtime+=end-start

	avgtime/=TRIALS
	average_times[s]=avgtime

print(f"[+]	Processed {l} Stations!")

copypasteoutput=""
for k,v in average_times.items():
	r=format(round(v,4), '.4f')
	copypasteoutput += f"{k}	{r}\n"
	print(f"Stations: {k}	Avg Execution Time: {r}\n")

#will only work on mac, i think you can use clip on win????
subprocess.run("pbcopy", text=True, input=copypasteoutput)

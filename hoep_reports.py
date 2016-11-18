from urllib import request
import os



def download(path):
	file_name = os.path.basename(path)

	print("Downloading data file from {}".format(path))
	try:
		mfile = request.urlopen(path)

		with open(file_name, 'wb') as handle:
			handle.write(mfile.read())

	except URLError:
		print("Timout while downloading <{}>".format(path))

	return os.path.abspath(file_name)





# url "http://reports.ieso.ca/public/DispUnconsHOEP/PUB_DispUnconsHOEP_20161002.xml"

base_url = "http://reports.ieso.ca/public/DispUnconsHOEP/PUB_DispUnconsHOEP_2016{:02d}{:02d}.xml"

print(list(range(1,32)))


url = base_url.format(8,1)


download(url)

#
# for day in range(1,32):
#     url = base_url.format(10, day)
#
#     download(url)

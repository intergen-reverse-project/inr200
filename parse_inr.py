from sys import argv
from pprint import pprint


try:
	filename = argv[1]
except IndexError:
	filename = 'test1.inr'

with open(filename, 'r') as fd:
	input_lines = fd.read().splitlines()

model = dict()
i = -1
while (i + 1) < len(input_lines):
	i += 1
	record_type, record_raw = input_lines[i].split(',', 1)
	try:
		record_type = int(record_type)
	except ValueError:
		continue  # TODO - clear
		raise ValueError('\n'.join([
			f'[line {i+1}] Parse error - wrong record type',
			'Ex: This file must be converted to the latest format for use with this program.'
		]))

	if not record_raw:
		raise ValueError('\n'.join([
			f'[line {i+1}] Parse error - incomplete record {record_type}',
			'Ex: Incomplete data input file.'
		]))
	else:
		record_body = record_raw.split(',')

	if record_type == 100:
		if model.get('misc'):
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} duplicated')
		else:
			try:
				model['misc'] = {
					'height': int(record_body[0]),
					'lock_number_of_cylinders': bool(int(record_body[1])),
				}
			except:
				raise ValueError('\n'.join([
					f'[line {i+1}] Parse error - incomplete record {record_type}',
					'Ex: Incomplete data input file.'
				]))

	elif record_type == 101:
		if model.get('project_information'):
			raise ValueError(f'[line {i+1}] Parse error - record 101 duplicated')
		else:
			try:
				model['project_information'] = {
					'file_path': record_body[0].strip('"'),
					'job_number': record_body[1].strip('"'),
					'customer_name': record_body[2].strip('"'),
					'address': record_body[3].strip('"'),
					'address_continued': record_body[4].strip('"'),
					'city': record_body[5].strip('"'),
					'state_province': record_body[6].strip('"'),
					'postal_code': record_body[7].strip('"'),
					'country': record_body[8].strip('"'),
					'remarks': record_body[9].strip('"'),
				}
			except:
				raise ValueError('\n'.join([
					f'[line {i+1}] Parse error - incomplete record {record_type}',
					'Ex: Incomplete data input file.'
				]))

	elif record_type == 102:
		if model.get('system_parameters'):
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} duplicated')
		else:
			try:
				const_t = record_body[0].strip('"')
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , CONST_T')
			else:
				if const_t != 'T':
					raise ValueError(f'[line {i+1}] Parse error - record {record_type} , CONST_T')
			try:
				measure = record_body[1].strip('"')
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , MEASURE')
			else:
				if measure not in ('ENG', 'METRIC'):
					raise ValueError(f'[line {i+1}] Parse error - record {record_type} , MEASURE')
			try:
				discharge_time = float(record_body[2])
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , DISCHARGE_TIME')
			try:
				nozzle_options_letter = record_body[3].strip('"')
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , NOZZLE_OPTIONS')
			else:
				try:
					nozzle_options = {
						'N': 'quantity_of_agent',
						'Y': 'fixed_nozzle'
					}[nozzle_options_letter]
				except:
					raise ValueError(f'[line {i+1}] Parse error - record {record_type} , NOZZLE_OPTIONS')
			try:
				number_of_cylinders = int(record_body[4])
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , NUM_CYLINDERS')
			try:
				cylinder_volume = float(record_body[5])
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , DISCHARGE_TIME')
			try:
				pre_discharge_pipe_temperature = float(record_body[6])
			except:
				raise ValueError(f'[line {i+1}] Parse error - record {record_type} , DISCHARGE_TIME')

			model['system_parameters'] = {
				'const_t': const_t,
				'measure': measure,
				'discharge_time': discharge_time,
				'nozzle_options': nozzle_options,
				'number_of_cylinders': number_of_cylinders,
				'cylinder_volume': cylinder_volume,
				'pre_discharge_pipe_temperature': pre_discharge_pipe_temperature
			}

	elif record_type == 103:
		...
	elif record_type == 201:
		...
	else:
		continue  # TODO - clear
		raise ValueError('\n'.join([
			f'[line {i+1}] Parse error - wrong record type',
			'Ex: This file must be converted to the latest format for use with this program.'
		]))

pprint(model)

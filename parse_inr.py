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
		continue  # TODO - rid out
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
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , CYLINDER_VOLUME')

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
		if model.get('pipe_data') is None:
			model['pipe_data'] = list()

		if len(model['pipe_data']) >= 500:
			raise ValueError(f'[line {i+1}] Parse error - too much records {record_type}')

		try:
			section_start = int(record_body[0])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , SECTION_START')

		try:
			section_end = int(record_body[1])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , SECTION_END')

		try:
			pipe_length = int(record_body[2])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , PIPE_LENGTH')

		try:
			elevation = int(record_body[3])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , ELEVATION')

		try:
			pipe_type_string = record_body[4].strip('"')
			_pipe_type_temp = pipe_type_string.split('-')
			pipe_size = _pipe_type_temp[0].rstrip(' ')
			pipe_sched = _pipe_type_temp[1]
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , PIPE_TYPE')

		try:
			elbows = int(record_body[5])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , ELBOWS')

		try:
			thru_tee = int(record_body[6])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , THRU_TEE')

		try:
			side_tee = int(record_body[7])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , SIDE_TEE')

		try:
			coupling_or_unions = int(record_body[8])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , COUPLING_OR_UNIONS')

		if model['system_parameters']['nozzle_options'] == 'quantity_of_agent':
			quantity_param_key = 'quantity_of_agent'
		elif model['system_parameters']['nozzle_options'] == 'fixed_nozzle':
			quantity_param_key = 'nozzle_diameter'
		else:
			raise ValueError(f'[line {i+1}] Parse error - wrong NOZZLE_OPTIONS {model["system_parameters"]["nozzle_options"]}')

		try:
			quantity_param_value = float(record_body[9])
		except:
			raise ValueError(f'[line {i+1}] Parse error - record {record_type} , {quantity_param_key.upper()}')

		pipe_record = {
			'section_start': section_start,
			'section_end': section_end,
			'length': pipe_length,
			'elevation': elevation,
			'pipe_size': pipe_size,
			'pipe_sched': pipe_sched,
			'elbows': elbows,
			'thru_tee': thru_tee,
			'side_tee': side_tee,
			'coupling_or_unions': coupling_or_unions,
			quantity_param_key: quantity_param_value,
			'eql': None  # TODO - CMB_EQL_VALIDATE
		}

		# TODO - validate (checkNewSection)

		model['pipe_data'].append(pipe_record)
	elif record_type == 201:
		...
	else:
		continue  # TODO - clear
		raise ValueError('\n'.join([
			f'[line {i+1}] Parse error - wrong record type',
			'Ex: This file must be converted to the latest format for use with this program.'
		]))

pprint(model)

import nidaqmx

def configure_timed_edge_counter(duration, 
								count_chan = "/Dev3/ctr0", 
								time_chan = "/Dev3/ctr1"):

	ctr = nidaqmx.task.Task()
	ctr.ci_channels.add_ci_count_edges_chan(count_chan)

	timer = nidaqmx.task.Task()
	timer.co_channels.add_co_pulse_chan_time(time_chan,
		low_time = .0001,
		high_time = duration)

	ctr.triggers.pause_trigger.dig_lvl_src = time_chan.replace('ctr', 'Ctr') + 'InternalOutput')
	ctr.triggers.pause_trigger.trig_type = nidaqmx.constants.TriggerType.DIGITAL_LEVEL
	ctr.triggers.pause_trigger.dig_lvl_when = nidaqmx.constants.Level.LOW

	return ctr, timer

def do_timed_edge_counter(ctr, timer):
	ctr.start()
	timer.start()
	while(not timer.is_task_done()):
		continue
	counts = ctr.read()
	ctr.stop()
	timer.stop()
	return counts

def configure_gated_edge_counter(count_chan = "/Dev3/ctr0", 
								gate_chan = "/Dev3/PFI1"):

	ctr = nidaqmx.task.Task()
	ctr.ci_channels.add_ci_count_edges_chan(count_chan)

	ctr.triggers.pause_trigger.dig_lvl_src = gate_chan
	ctr.triggers.pause_trigger.trig_type = nidaqmx.constants.TriggerType.DIGITAL_LEVEL
	ctr.triggers.pause_trigger.dig_lvl_when = nidaqmx.constants.Level.LOW

	return ctr


def do_gated_edge_counter(ctr):
	ctr.start()
# Need to add some kind of delay to ensure the counter has time to finish 
	counts = ctr.read()
	ctr.stop()
	return counts

def configure_ao_voltage(volt_chan, min_v = -3, max_v = 3):
	ao = nidaqmx.task.Task()
	ao.add_ao_voltage_chan(volt_chan, min_v, max_v)
	return ao

def set_ao_voltage(ao_task, voltage):
	ao_task.write(voltage)


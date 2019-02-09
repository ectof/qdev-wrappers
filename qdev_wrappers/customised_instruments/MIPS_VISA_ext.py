from qcodes.instrument_drivers.oxford.MercuryiPS_VISA import MercuryiPS
from typing import Dict, Union, Optional, Callable, List, cast
import numpy as np
import time


class MercuryiPS_ext(MercuryiPS):

	def __init__(self, name, address,
				 field_limits=None,
				 **kwargs) -> None:

		super().__init__(name, address,
						 field_limits=field_limits, **kwargs)
		
		self.add_parameter('theta_saferamp',
						   label='Theta',
						   unit='degrees',
						   set_cmd=self._theta_saferamp_set,
						   get_cmd=self._theta_saferamp_get)
		
		self.add_parameter('r_saferamp',
						   label='B_Radius',
						   unit='T',
						   set_cmd=self._r_saferamp_set,
						   get_cmd=self._r_saferamp_get)

		self.add_parameter('r_simulramp',
						   label='B_Radius',
						   unit='T',
						   set_cmd=self._r_simulramp_set,
						   get_cmd=self._r_simulramp_get)

		self.add_parameter('phi_saferamp',
						   label='Phi',
						   unit='degrees',
						   set_cmd=self._phi_saferamp_set,
						   get_cmd=self._phi_saferamp_get)

	def ramp(self, mode: str="safe") -> None:
		"""
		Ramp the fields to their present target value

		Args:
			mode: how to ramp, either 'simul' or 'safe'. In 'simul' mode,
			  the fields are ramping simultaneously in a non-blocking mode.
			  There is no safety check that the safe zone is not exceeded. In
			  'safe' mode, the fields are ramped one-by-one in a blocking way
			  that ensures that the total field stays within the safe region
			  (provided that this region is convex).
		"""
		if mode not in ['simul', 'safe', 'simul_block']:
			raise ValueError('Invalid ramp mode. Please provide either "simul"'
							 ',"safe" or "simul_block".')

		meas_vals = self._get_measured(['x', 'y', 'z'])
		# we asked for three coordinates, so we know that we got a list
		meas_vals = cast(List[float], meas_vals)

		for cur, slave in zip(meas_vals, self.submodules.values()):
			if slave.field_target() != cur:
				if slave.field_ramp_rate() == 0:
					raise ValueError(f'Can not ramp {slave}; ramp rate set to'
									 ' zero!')

		# then the actual ramp
		{'simul': self._ramp_simultaneously,
		 'safe': self._ramp_safely,
		 'simul_block':self._ramp_simultaneously_blocking}[mode]()


	def _ramp_simultaneously_blocking(self) -> None:
		"""
		Ramp all three fields to their target simultaneously at their given
		ramp rates. NOTE: there is NO guarantee that this does not take you
		out of your safe region. Use with care.
		"""
		for slave in self.submodules.values():
			slave.ramp_to_target()

		for slave in np.array(list(self.submodules.values())):
			# wait for the ramp to finish, we don't car about the order
			while slave.ramp_status() == 'TO SET':
				time.sleep(0.1)

	def _theta_saferamp_set(self, target):
		"""
		Set the theta target and ramp to it
		"""
		self.theta_target(target)
		self.ramp(mode='safe')
		self.theta_measured()

	def _theta_saferamp_get(self):
		"""
		Get the measured theta
		"""
		return self.theta_measured()

	def _r_saferamp_set(self, target):
		"""
		Set the radius target and ramp to it
		"""
		self.r_target(target)
		self.ramp(mode='safe')
		self.r_measured()

	def _r_saferamp_get(self):
		"""
		Get the measured radius
		"""
		return self.r_measured()

	def _r_simulramp_set(self, target):
		"""
		Set the radius target and ramp to it
		"""
		self.r_target(target)
		self.ramp(mode='simul_block')
		self.r_measured()

	def _r_simulramp_get(self):
		"""
		Get the measured radius
		"""
		return self.r_measured()

	def _phi_saferamp_set(self, target):
		"""
		Set the theta target and ramp to it
		"""
		self.phi_target(target)
		self.ramp(mode='safe')
		self.phi_measured()

	def _phi_saferamp_get(self):
		"""
		Get the measured theta
		"""
		return self.phi_measured()
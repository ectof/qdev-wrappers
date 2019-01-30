from qcodes.instrument_drivers.oxford.MercuryiPS_VISA import MercuryiPS


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
						   unit='Tesla',
						   set_cmd=self._r_saferamp_set,
						   get_cmd=self._r_saferamp_get)

		self.add_parameter('phi_saferamp',
		                   label='B_Radius',
						   unit='Tesla',
						   set_cmd=self._phi_saferamp_set,
						   get_cmd=self._phi_saferamp_get)

	def _theta_saferamp_set(self, target):
		"""
		Set the theta target and ramp to it
		"""
		self.theta_target(target)
		self.ramp(mode='safe')
		self.theta_measured.get()

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
		self.r_measured.get()

	def _r_saferamp_get(self):
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
		self.phi_measured.get()

	def _phi_saferamp_get(self):
		"""
		Get the measured theta
		"""
		return self.phi_measured()
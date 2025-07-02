# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from numpy import ndarray
from typing import TYPE_CHECKING, Optional, Literal
from pyucalgarysrs.exceptions import SRSAPIError
from pyucalgarysrs.models.atm import (
    ATMForwardOutputFlags,
    ATMForwardResult,
    ATMInverseOutputFlags,
    ATMInverseResult,
    ATM_DEFAULT_MAXWELLIAN_ENERGY_FLUX,
    ATM_DEFAULT_MAXWELLIAN_CHARACTERISTIC_ENERGY,
    ATM_DEFAULT_GAUSSIAN_ENERGY_FLUX,
    ATM_DEFAULT_GAUSSIAN_PEAK_ENERGY,
    ATM_DEFAULT_GAUSSIAN_SPECTRAL_WIDTH,
    ATM_DEFAULT_KAPPA_ENERGY_FLUX,
    ATM_DEFAULT_KAPPA_MEAN_ENERGY,
    ATM_DEFAULT_KAPPA_K_INDEX,
    ATM_DEFAULT_EXPONENTIAL_ENERGY_FLUX,
    ATM_DEFAULT_EXPONENTIAL_CHARACTERISTIC_ENERGY,
    ATM_DEFAULT_EXPONENTIAL_STARTING_ENERGY,
    ATM_DEFAULT_PROTON_ENERGY_FLUX,
    ATM_DEFAULT_PROTON_CHARACTERISTIC_ENERGY,
    ATM_DEFAULT_D_REGION_FLAG,
    ATM_DEFAULT_NRLMSIS_MODEL_VERSION,
    ATM_DEFAULT_OXYGEN_CORRECTION_FACTOR,
    ATM_DEFAULT_TIMESCALE_AURORAL,
    ATM_DEFAULT_TIMESCALE_TRANSPORT,
    ATM_DEFAULT_MODEL_VERSION,
    ATM_DEFAULT_PRECIPITATION_SPECTRAL_FLUX_TYPE,
)
from ...exceptions import AuroraXAPIError
if TYPE_CHECKING:
    from ...pyaurorax import PyAuroraX  # pragma: nocover-ok

__all__ = [
    "ATMManager",
]


class ATMManager:
    """
    The ATMManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj: PyAuroraX = aurorax_obj

    def forward(self,
                timestamp: datetime.datetime,
                geodetic_latitude: float,
                geodetic_longitude: float,
                output: ATMForwardOutputFlags,
                maxwellian_energy_flux: float = ATM_DEFAULT_MAXWELLIAN_ENERGY_FLUX,
                maxwellian_characteristic_energy: float = ATM_DEFAULT_MAXWELLIAN_CHARACTERISTIC_ENERGY,
                gaussian_energy_flux: float = ATM_DEFAULT_GAUSSIAN_ENERGY_FLUX,
                gaussian_peak_energy: float = ATM_DEFAULT_GAUSSIAN_PEAK_ENERGY,
                gaussian_spectral_width: float = ATM_DEFAULT_GAUSSIAN_SPECTRAL_WIDTH,
                kappa_energy_flux: float = ATM_DEFAULT_KAPPA_ENERGY_FLUX,
                kappa_mean_energy: float = ATM_DEFAULT_KAPPA_MEAN_ENERGY,
                kappa_k_index: float = ATM_DEFAULT_KAPPA_K_INDEX,
                exponential_energy_flux: float = ATM_DEFAULT_EXPONENTIAL_ENERGY_FLUX,
                exponential_characteristic_energy: float = ATM_DEFAULT_EXPONENTIAL_CHARACTERISTIC_ENERGY,
                exponential_starting_energy: float = ATM_DEFAULT_EXPONENTIAL_STARTING_ENERGY,
                proton_energy_flux: float = ATM_DEFAULT_PROTON_ENERGY_FLUX,
                proton_characteristic_energy: float = ATM_DEFAULT_PROTON_CHARACTERISTIC_ENERGY,
                d_region: bool = ATM_DEFAULT_D_REGION_FLAG,
                nrlmsis_model_version: Literal["00", "2.0"] = ATM_DEFAULT_NRLMSIS_MODEL_VERSION,
                oxygen_correction_factor: float = ATM_DEFAULT_OXYGEN_CORRECTION_FACTOR,
                timescale_auroral: int = ATM_DEFAULT_TIMESCALE_AURORAL,
                timescale_transport: int = ATM_DEFAULT_TIMESCALE_TRANSPORT,
                atm_model_version: Literal["1.0", "2.0"] = ATM_DEFAULT_MODEL_VERSION,
                custom_spectrum: Optional[ndarray] = None,
                custom_neutral_profile: Optional[ndarray] = None,
                no_cache: bool = False,
                timeout: Optional[int] = None) -> ATMForwardResult:
        """
        Perform a forward calculation using the TREx Auroral Transport Model and the supplied input 
        parameters. Note that this function utilizes the UCalgary Space Remote Sensing API to perform 
        the calculation.

        The ATM model is 1D and time-independent. However, the optional parameters `timescale_auroral` 
        and `timescale_transport` provide limited support for time-dependent and transport process. The
        `timescale_auroral` parameter (T0) is the duration of the precipitation. The `timescale_transport` 
        parameter is defined by L/v0, in which L is the dimension of the auroral structure, and v0 is the 
        cross-structure drift speed. The model quasi-analytically solves the continuity equation under a 
        square input (with time duration T0 and spatial width L) input of precipitation. The initial/boundary 
        conditions are given by IRI. The output yields the mean density/VER over [0-L] at time T0.

        Please note that some of the inputs and outputs are only supported by ATM version 2.0. The following
        inputs are only supported by version 2.0: `kappa_*`, `exponential_*`, `proton_*`, `d_region`, and 
        `custom_neutral_profile`. The following outputs are only supported by version 2.0: `production_rate_*`.

        **NOTE**: All spectral shapes are super-imposable except exponential (maxwellian, gaussian, kappa). The 
        exponential spectrum should be only be used for high-energy tail and, starting from E0 (proton_starting_energy), 
        will override any other spectral specification.

        **NOTE**: proton precipitation is presently only for ionization rate and density calculations. Proton auroras are 
        not nominal TREx characteristics and currently not computed in this version of the model.

        **NOTE**: when using the d_region flag, enabling proton parameters is not permitted.

        Args:
            timestamp (datetime.datetime): 
                Timestamp for the calculation. This value is expected to be in UTC, and is valid for any value up to the 
                end of the previous day. Any timezone data will be ignored. This parameter is required.

            geodetic_latitude (float): 
                Latitude in geodetic coordinates: -90.0 to 90.0. This parameter is required.

            geodetic_longitude (float): 
                Longitude in geodetic coordinates: -180.0 to 180.0. This parameter is required.

            output (ATMForwardOutputFlags): 
                Flags to indicate which values are included in the output. See 
                [`ATMForwardOutputFlags`](https://docs-pyucalgarysrs.phys.ucalgary.ca/models/atm/classes_forward.html#pyucalgarysrs.models.atm.classes_forward.ATMForwardOutputFlags) 
                for more details. This parameter is required.

            maxwellian_energy_flux (float): 
                Maxwellian energy flux in erg/cm2/s. Default is 10. This parameter is optional.

            maxwellian_characteristic_energy (float): 
                Maxwellian characteristic energy in eV. Default is 5000. Note that `maxwellian_characteristic_energy` 
                should be specified if the `maxwellian_energy_flux` is not 0. If it is not, then the default will be used. This 
                parameter is optional.

            gaussian_energy_flux (float): 
                Gaussian energy flux in erg/cm2/s. Default is 0, meaning all gaussian parameters will be disabled. 
                Note that `gaussian_peak_energy` and `gaussian_spectral_width` should be specified if the `gaussian_energy_flux` 
                is not 0. If they are not, then their defaults will be used. This parameter is optional.

            gaussian_peak_energy (float): 
                Gaussian peak energy in eV. Default is 1000. Note this parameter should be specified if the `gaussian_energy_flux` 
                is not 0. This parameter is optional.

            gaussian_spectral_width (float): 
                Gaussian spectral width in eV. Default is 100. Note this parameter should be specified if the `gaussian_energy_flux` 
                is not 0. This parameter is optional.

            kappa_energy_flux (float): 
                Kappa energy flux in erg/cm2/s. Default is 0, meaning all kappa parameters will be disabled. Note that 
                `kappa_mean_energy` and `kappa_k_index` should be specified if `kappa_energy_flux` is not 0. If they are not, then
                their defaults will be used. This parameter is optional.

            kappa_mean_energy (float): 
                Kappa mean energy in eV. Default is 30000. Note this parameter should be specified if the `kappa_energy_flux` 
                is not 0. This parameter is optional.

            kappa_k_index (float): 
                Kappa k-index. Default is 5. Note this parameter should be specified if the `kappa_energy_flux` is not 0. This 
                parameter is optional.

            exponential_energy_flux (float): 
                Exponential energy flux, in erg/cm2/s. Default is 0, meaning all exponential parameters will be disabled. Note that
                `exponential_characteristic_energy` and `exponential_starting_energy` should be specified if `exponential_energy_flux` 
                is not 0. If it is not, then the default will be used. This parameter is optional.

            exponential_characteristic_energy (float): 
                Exponential characteristic energy, in eV. Default is 50000. Note this parameter should be specified if the 
                `exponential_energy_flux` is not 0. This parameter is optional.

            exponential_starting_energy (float): 
                Exponential starting energy, in eV. Default is 50000. Note this parameter should be specified if the 
                `exponential_energy_flux` is not 0. This parameter is optional.

            proton_energy_flux (float): 
                Proton energy flux, in erg/cm2/s. Default is 0, meaning all proton parameters will be disabled. Note that
                `proton_characteristic_energy` should be specified if `proton_energy_flux` is not 0. If it is not, then the default
                will be used. This parameter is optional.

            proton_characteristic_energy (float): 
                Proton characteristic energy, in eV. Default is 10000. Not this parameter should be specified if the 
                `proton_energy_flux` is not 0. This parameter is optional.

            d_region (bool): 
                Flag to enable D-region evaluation. Default is False. 

            nrlmsis_model_version (str): 
                NRLMSIS version number. Possible values are `00` or `2.0`. Default is `2.0`. This parameter is
                optional. More details about this empirical model can be found [here](https://ccmc.gsfc.nasa.gov/models/NRLMSIS~00/),
                and [here](https://ccmc.gsfc.nasa.gov/models/NRLMSIS~2.0/).

            oxygen_correction_factor (float): 
                Oxygen correction factor used to multiply by in the empirical model. Default is 1. This parameter
                is optional.

            custom_spectrum (ndarray): 
                A 2-dimensional numpy array (dtype is any float type) containing values representing the
                energy in eV, and flux in 1/cm2/sr/eV. The shape is expected to be [N, 2], with energy in
                [:, 0] and flux in [:, 1]. Note that this array cannot contain negative values (SRSAPIError 
                will be raised if so). This parameter is optional.

            custom_neutral_profile (ndarray): 
                A 2-D numpy array (dtype is any float type) containing values representing altitude, densities for O, O2, N2, N, 
                and NO, and lastly temperature. Altitude is expected to be in kilometers, all densities in cm^-3, and 
                temperature in Kelvin. This parameter is optional.

                The shape of the array is expected to be [N, 7], with the order matching the above mentioned values. Note that
                this array cannot contain and negative values (SRSAPIError will be raised if so).
                
                Users are responsible for fully covering the altitude range of interest in the provided profile (80-800 km if 
                d_region_flag=0, or 50-500 km if d_region_flag=1). The model only performs interpolation, not extrapolation.

            timescale_auroral (int): 
                The duration of the precipitation, in seconds. Default is 600 (10 minutes). This parameter is optional.

            timescale_transport (int): 
                Defined by L/v0, in which L is the dimension of the auroral structure, and v0 is the cross-structure drift 
                speed. Represented in seconds. Default is 600 (10 minutes). This parameter is optional.

            atm_model_version (str): 
                ATM model version number. Possible values are presently "1.0" or "2.0". The default is "2.0". This parameter is
                optional.
                
                **IMPORTANT**: Please note that certain inputs and outputs are only available in version "2.0". See above for 
                more details.

            no_cache (bool): 
                The UCalgary Space Remote Sensing API utilizes a caching layer for performing ATM
                calculations. If this variation of input parameters has been run before (and the
                cache is still valid), then it will not re-run the calculation. Instead it will 
                return the cached results immediately. To disable the caching layer, set this 
                parameter to `True`. Default is `False`. This parameter is optional.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            An [`ATMForwardResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/models/atm/classes_forward.html#pyucalgarysrs.models.atm.classes_forward.ATMForwardResult)
            object containing the requested output data, among other values.

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        try:
            return self.__aurorax_obj.srs_obj.models.atm.forward(
                timestamp,
                geodetic_latitude,
                geodetic_longitude,
                output,
                maxwellian_energy_flux=maxwellian_energy_flux,
                maxwellian_characteristic_energy=maxwellian_characteristic_energy,
                gaussian_energy_flux=gaussian_energy_flux,
                gaussian_peak_energy=gaussian_peak_energy,
                gaussian_spectral_width=gaussian_spectral_width,
                kappa_energy_flux=kappa_energy_flux,
                kappa_mean_energy=kappa_mean_energy,
                kappa_k_index=kappa_k_index,
                exponential_energy_flux=exponential_energy_flux,
                exponential_characteristic_energy=exponential_characteristic_energy,
                exponential_starting_energy=exponential_starting_energy,
                proton_energy_flux=proton_energy_flux,
                proton_characteristic_energy=proton_characteristic_energy,
                d_region=d_region,
                nrlmsis_model_version=nrlmsis_model_version,
                oxygen_correction_factor=oxygen_correction_factor,
                custom_spectrum=custom_spectrum,
                custom_neutral_profile=custom_neutral_profile,
                timescale_auroral=timescale_auroral,
                timescale_transport=timescale_transport,
                atm_model_version=atm_model_version,
                no_cache=no_cache,
                timeout=timeout,
            )
        except SRSAPIError as e:  # pragma: nocover
            raise AuroraXAPIError(e) from e

    def inverse(self,
                timestamp: datetime.datetime,
                geodetic_latitude: float,
                geodetic_longitude: float,
                intensity_4278: float,
                intensity_5577: float,
                intensity_6300: float,
                intensity_8446: float,
                output: ATMInverseOutputFlags,
                precipitation_flux_spectral_type: Literal["gaussian", "maxwellian"] = ATM_DEFAULT_PRECIPITATION_SPECTRAL_FLUX_TYPE,
                nrlmsis_model_version: Literal["00", "2.0"] = ATM_DEFAULT_NRLMSIS_MODEL_VERSION,
                atmospheric_attenuation_correction: bool = False,
                atm_model_version: Literal["1.0", "2.0"] = ATM_DEFAULT_MODEL_VERSION,
                no_cache: bool = False,
                timeout: Optional[int] = None) -> ATMInverseResult:
        """
        Perform an inverse calculation using the TREx Auroral Transport Model and the supplied input 
        parameters. Note that this function utilizes the UCalgary Space Remote Sensing API to perform 
        the calculation.

        **NOTE**: The 'atmospheric_attenuation_correction' parameter has been deprecated. Please ensure you perform 
        this conversion yourself on the results, if desired.

        Args:
            timestamp (datetime.datetime): 
                Timestamp for the calculation. This value is expected to be in UTC, and is valid for a pre-defined 
                timeframe. An error will be raised if outside of the valid timeframe. Any timezone data will be 
                ignored. This parameter is required.

            geodetic_latitude (float): 
                Latitude in geodetic coordinates. Currently limited to the Transition Region Explorer (TREx)
                region of >=50.0 and <71.5 degrees. An error will be raised if outside of this range. This 
                parameter is required.

            geodetic_longitude (float): 
                Longitude in geodetic coordinates. Currently limited to the Transition Region Explorer (TREx)
                region of >=-160 and <-75 degrees. An error will be raised if outside of this range. This 
                parameter is required.

            intensity_4278 (float): 
                Intensity of the 427.8nm (blue) wavelength. This is expected to be a height-integrated value, 
                represented in Rayleighs. This parameter is required.

            intensity_5577 (float): 
                Intensity of the 557.7nm (green) wavelength. This is expected to be a height-integrated value, 
                represented in Rayleighs. This parameter is required.

            intensity_6300 (float): 
                Intensity of the 630.0nm (red) wavelength. This is expected to be a height-integrated value, 
                represented in Rayleighs. This parameter is required.

            intensity_8446 (float): 
                Intensity of the 844.6nm (near infrared) wavelength. This is expected to be a height-integrated value, 
                represented in Rayleighs. This parameter is required.

            output (ATMInverseOutputFlags): 
                Flags to indicate which values are included in the output. See 
                [`ATMInverseOutputFlags`](https://docs-pyucalgarysrs.phys.ucalgary.ca/models/atm/classes_inverse.html#pyucalgarysrs.models.atm.classes_inverse.ATMInverseOutputFlags) 
                for more details. This parameter is required.

            precipitation_flux_spectral_type (str): 
                The precipitation flux spectral type to use. Possible values are `gaussian` or `maxwellian`. The
                default is `gaussian`. This parameter is optional.

            nrlmsis_model_version (str): 
                NRLMSIS version number. Possible values are `00` or `2.0`. Default is `2.0`. This parameter is
                optional. More details about this empirical model can be found [here](https://ccmc.gsfc.nasa.gov/models/NRLMSIS~00/),
                and [here](https://ccmc.gsfc.nasa.gov/models/NRLMSIS~2.0/).

            atmospheric_attenuation_correction (bool): 
                Apply an atmospheric attenuation correction factor. Default is `False`.

                This parameter has been deprecated and will be removed in a future release.

            atm_model_version (str): 
                ATM model version number. Possible values are presently "1.0" or "2.0". The default is "2.0". This parameter is 
                optional.
                
                **IMPORTANT**: Please note that certain inputs and outputs are only available in version "2.0". See above for 
                more details.

            no_cache (bool): 
                The UCalgary Space Remote Sensing API utilizes a caching layer for performing ATM
                calculations. If this variation of input parameters has been run before (and the
                cache is still valid), then it will not re-run the calculation. Instead it will 
                return the cached results immediately. To disable the caching layer, set this 
                parameter to `True`. Default is `False`. This parameter is optional.

            timeout (int): 
                Represents how many seconds to wait for the API to send data before giving up. The 
                default is 10 seconds, or the `api_timeout` value in the super class' `pyaurorax.PyAuroraX`
                object. This parameter is optional.

        Returns:
            An [`ATMInverseResult`](https://docs-pyucalgarysrs.phys.ucalgary.ca/models/atm/classes_inverse.html#pyucalgarysrs.models.atm.classes_inverse.ATMInverseResult)
            object containing the requested output data, among other values.

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        try:
            return self.__aurorax_obj.srs_obj.models.atm.inverse(
                timestamp,
                geodetic_latitude,
                geodetic_longitude,
                intensity_4278,
                intensity_5577,
                intensity_6300,
                intensity_8446,
                output,
                precipitation_flux_spectral_type=precipitation_flux_spectral_type,
                nrlmsis_model_version=nrlmsis_model_version,
                atm_model_version=atm_model_version,
                atmospheric_attenuation_correction=atmospheric_attenuation_correction,
                no_cache=no_cache,
                timeout=timeout,
            )
        except SRSAPIError as e:  # pragma: nocover
            raise AuroraXAPIError(e) from e

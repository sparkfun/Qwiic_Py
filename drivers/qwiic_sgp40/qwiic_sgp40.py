#-----------------------------------------------------------------------------
# qwiic_sgp40.py
#
# Python library for the SparkFun Air Quality Sensor - SGP40 (Qwiic).
#   https://www.sparkfun.com/products/18345
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# This python module heavily is heavily based on the driver written by 
# DFRobot and leverages its VOC algorithm. It can be found here:
# https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

"""!
qwiic_sgp40
===========
Python module for the SparkFun Air Quality Sensor - SGP40 (Qwiic).

This package is a port of the existing [SparkFun SGP40 Arduino Library](https://github.com/sparkfun/SparkFun_SGP40_Arduino_Library) and is heavily based on the driver written by [DFRobot](https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi).

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ----------------------------------------------------------------------

import qwiic_i2c

__version__ = "3.0.0"

# ----------------------------------------------------------------------
# VOC Index algorithm
#
# Ported from the DFRobot SGP40 Python driver,
# https://github.com/DFRobot/DFRobot_SGP40 (Python/raspberrypi/DFRobot_SGP40_VOCAlgorithm.py),
# with its names made private. Its license:
#
# Copyright 2010 DFRobot Co.Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------

_VOCALGORITHM_SAMPLING_INTERVAL                           = (1.)
_VOCALGORITHM_INITIAL_BLACKOUT                            = (45.)
_VOCALGORITHM_VOC_INDEX_GAIN                              = (230.)
_VOCALGORITHM_SRAW_STD_INITIAL                            = (50.)
_VOCALGORITHM_SRAW_STD_BONUS                              = (220.)
_VOCALGORITHM_TAU_MEAN_VARIANCE_HOURS                     = (12.)
_VOCALGORITHM_TAU_INITIAL_MEAN                            = (20.)
_VOCALGORITHM_INITI_DURATION_MEAN                          = (3600. * 0.75)
_VOCALGORITHM_INITI_TRANSITION_MEAN                        = (0.01)
_VOCALGORITHM_TAU_INITIAL_VARIANCE                        = (2500.)
_VOCALGORITHM_INITI_DURATION_VARIANCE                      = ((3600. * 1.45))
_VOCALGORITHM_INITI_TRANSITION_VARIANCE                    = (0.01)
_VOCALGORITHM_GATING_THRESHOLD                            = (340.)
_VOCALGORITHM_GATING_THRESHOLD_INITIAL                    = (510.)
_VOCALGORITHM_GATING_THRESHOLD_TRANSITION                 = (0.09)
_VOCALGORITHM_GATING_MAX_DURATION_MINUTES                 = ((60. * 3.))
_VOCALGORITHM_GATING_MAX_RATIO                            = (0.3)
_VOCALGORITHM_SIGMOID_L                                   = (500.)
_VOCALGORITHM_SIGMOID_K                                   = (-0.0065)
_VOCALGORITHM_SIGMOID_X0                                  = (213.)
_VOCALGORITHM_VOC_INDEX_OFFSET_DEFAULT                    = (100.)
_VOCALGORITHM_LP_TAU_FAST                                 = (20.0)
_VOCALGORITHM_LP_TAU_SLOW                                 = (500.0)
_VOCALGORITHM_LP_ALPHA                                    = (-0.2)
_VOCALGORITHM_PERSISTENCE_UPTIME_GAMMA                    = ((3. * 3600.))
_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING      = (64.)
_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX          = (32767.)
_FIX16_MAXIMUM                                            = 0x7FFFFFFF
_FIX16_MINIMUM                                            = 0x80000000
_FIX16_OVERFLOW                                           = 0x80000000
_FIX16_ONE                                                = 0x00010000

class _DFRobotVOCAlgorithmParams(object):
    def __init__(self):
        self.mvoc_index_offset = 0
        self.mtau_mean_variance_hours = 0
        self.mgating_max_duration_minutes = 0
        self.msraw_std_initial=0
        self.muptime=0
        self.msraw=0
        self.mvoc_index=0
        self.m_mean_variance_estimator_gating_max_duration_minutes=0
        self.m_mean_variance_estimator_initialized=0
        self.m_mean_variance_estimator_mean=0
        self.m_mean_variance_estimator_sraw_offset=0
        self.m_mean_variance_estimator_std=0
        self.m_mean_variance_estimator_gamma=0
        self.m_mean_variance_estimator_gamma_initial_mean=0
        self.m_mean_variance_estimator_gamma_initial_variance=0
        self.m_mean_variance_estimator_gamma_mean=0
        self.m_mean_variance_estimator__gamma_variance=0
        self.m_mean_variance_estimator_uptime_gamma=0
        self.m_mean_variance_estimator_uptime_gating=0
        self.m_mean_variance_estimator_gating_duration_minutes=0
        self.m_mean_variance_estimator_sigmoid_l=0
        self.m_mean_variance_estimator_sigmoid_k=0
        self.m_mean_variance_estimator_sigmoid_x0=0
        self.m_mox_model_sraw_mean=0
        self.m_sigmoid_scaled_offset=0
        self.m_adaptive_lowpass_a1=0
        self.m_adaptive_lowpass_a2=0
        self.m_adaptive_lowpass_initialized=0
        self.m_adaptive_lowpass_x1=0
        self.m_adaptive_lowpass_x2=0
        self.m_adaptive_lowpass_x3=0

class _DFRobotVOCAlgorithm(object):
    
    def __init__(self):
        self.params = _DFRobotVOCAlgorithmParams()
    def _f16(self,x):
        if x >= 0:
            return int((x)*65536.0 + 0.5)
        else:
            return int((x)*65536.0 - 0.5)

    def _fix16_from_int(self,a):
        return int(a * _FIX16_ONE)

    def _fix16_cast_to_int(self,a):
        return int(a) >> 16

    def _fix16_mul(self,inarg0,inarg1):
        inarg0=int(inarg0)
        inarg1=int(inarg1)
        A = (inarg0 >> 16)
        if inarg0<0:
            B = (inarg0&0xFFFFFFFF) & 0xFFFF
        else:
            B = inarg0&0xFFFF
        C = (inarg1 >> 16)
        if inarg1<0:
            D = (inarg1&0xFFFFFFFF) & 0xFFFF
        else:
            D = inarg1&0xFFFF
        AC = (A * C)
        AD_CB = (A * D + C * B)
        BD = (B * D)
        product_hi = (AC + (AD_CB >> 16))
        ad_cb_temp = ((AD_CB) << 16)&0xFFFFFFFF
        product_lo = ((BD + ad_cb_temp))&0xFFFFFFFF
        if product_lo < BD :
            product_hi =product_hi+1
        if ((product_hi >> 31) != (product_hi >>15)):
            return _FIX16_OVERFLOW
        product_lo_tmp = product_lo&0xFFFFFFFF
        product_lo = (product_lo - 0x8000)&0xFFFFFFFF
        product_lo = (product_lo-((product_hi&0xFFFFFFFF) >> 31))&0xFFFFFFFF
        if product_lo > product_lo_tmp:
            product_hi = product_hi-1
        result = (product_hi << 16)|(product_lo >> 16)
        result +=1
        return result
    
    def _fix16_div(self,a, b):
        a=int(a)
        b=int(b)
        if b==0 :
            return _FIX16_MINIMUM
        if a>=0:
            remainder = a
        else:
            remainder = (a*(-1))&0xFFFFFFFF
        if b >= 0:
            divider = b
        else:
            divider = (b*(-1))&0xFFFFFFFF
        quotient = 0
        bit =0x10000
        while (divider < remainder):
            divider = divider<<1
            bit <<= 1
        if not bit:
            return _FIX16_OVERFLOW
        if (divider & 0x80000000):
            if (remainder >= divider):
                quotient |= bit
                remainder -= divider
            divider >>= 1
            bit >>= 1
        while bit and remainder:
            if (remainder >= divider):
                quotient |= bit    
                remainder -= divider
            remainder <<= 1
            bit >>= 1
        if (remainder >= divider):
            quotient+=1
        result = quotient
        if ((a ^ b) & 0x80000000):
            if (result == _FIX16_MINIMUM):
                return _FIX16_OVERFLOW
            result = -result
        return result
    
    def _fix16_sqrt(self,x):
        x=int(x)
        num=x&0xFFFFFFFF
        result = 0
        bit = 1 << 30
        while (bit > num):
            bit >>=2
        for n in range(0,2):
            while (bit):
                if (num >= result + bit):
                    num = num-(result + bit)&0xFFFFFFFF
                    result = (result >> 1) + bit
                else:
                    result = (result >> 1)
                bit >>= 2
            if n==0:
                if num > 65535:
                    num = (num -result)&0xFFFFFFFF
                    num = ((num << 16) - 0x8000)&0xFFFFFFFF
                    result = ((result << 16) + 0x8000)&0xFFFFFFFF
                else:
                    num = ((num << 16)&0xFFFFFFFF)
                    result =((result << 16)&0xFFFFFFFF)
                bit = 1 << 14
        if (num > result):
                result+=1
        return result
    
    def _fix16_exp(self,x):
        x=int(x)
        exp_pos_values=[self._f16(2.7182818), self._f16(1.1331485), self._f16(1.0157477), self._f16(1.0019550)]
        exp_neg_values=[self._f16(0.3678794), self._f16(0.8824969), self._f16(0.9844964), self._f16(0.9980488)]
        if (x >= self._f16(10.3972)):
            return _FIX16_MAXIMUM
        if (x <= self._f16(-11.7835)):
            return 0
        if (x < 0):
            x = -x
            exp_values = exp_neg_values
        else:
            exp_values = exp_pos_values
        res = _FIX16_ONE
        arg = _FIX16_ONE
        for i in range(0,4):
            while (x >= arg):
                res = self._fix16_mul(res, exp_values[i]);
                x -= arg;
            arg >>=3
        return res
    
    def vocalgorithm_init(self):
        self.params.mvoc_index_offset = (self._f16(_VOCALGORITHM_VOC_INDEX_OFFSET_DEFAULT))
        self.params.mtau_mean_variance_hours = self._f16(_VOCALGORITHM_TAU_MEAN_VARIANCE_HOURS)
        self.params.mgating_max_duration_minutes =self._f16(_VOCALGORITHM_GATING_MAX_DURATION_MINUTES)
        self.params.msraw_std_initial = self._f16(_VOCALGORITHM_SRAW_STD_INITIAL)
        self.params.muptime = self._f16(0.)
        self.params.msraw = self._f16(0.)
        self.params.mvoc_index = 0
        self._vocalgorithm__init_instances()
    
    def _vocalgorithm__init_instances(self):
        self._vocalgorithm__mean_variance_estimator__init()
        self._vocalgorithm__mean_variance_estimator__set_parameters(self._f16(_VOCALGORITHM_SRAW_STD_INITIAL), self.params.mtau_mean_variance_hours,self.params.mgating_max_duration_minutes)
        self._vocalgorithm__mox_model__init()
        self._vocalgorithm__mox_model__set_parameters(self._vocalgorithm__mean_variance_estimator__get_std(),self._vocalgorithm__mean_variance_estimator__get_mean())
        self._vocalgorithm__sigmoid_scaled__init()
        self._vocalgorithm__sigmoid_scaled__set_parameters(self.params.mvoc_index_offset)
        self._vocalgorithm__adaptive_lowpass__init()
        self._vocalgorithm__adaptive_lowpass__set_parameters()
    
    def _vocalgorithm_get_states(self,state0,state1):
        state0 = self._vocalgorithm__mean_variance_estimator__get_mean()
        state1 = self._vocalgorithm__mean_variance_estimator__get_std()
        return state0,state1
    
    def _vocalgorithm_set_states(self,state0,state1):
        self._vocalgorithm__mean_variance_estimator__set_states(self.params, state0, state1, self._f16(_VOCALGORITHM_PERSISTENCE_UPTIME_GAMMA))
        self.params.msraw = state0
    
    def _vocalgorithm_set_tuning_parameters(self, voc_index_offset, learning_time_hours, gating_max_duration_minutes, std_initial):
        self.params.mvoc_index_offset = self._fix16_from_int(voc_index_offset)
        self.params.mtau_mean_variance_hours = self._fix16_from_int(learning_time_hours)
        self.params.mgating_max_duration_minutes =self._fix16_from_int(gating_max_duration_minutes)
        self.params.msraw_std_initial = self._fix16_from_int(std_initial)
        self._vocalgorithm__init_instances();
    
    def vocalgorithm_process(self, sraw):
        if ((self.params.muptime <= self._f16(_VOCALGORITHM_INITIAL_BLACKOUT))):
            self.params.muptime = self.params.muptime + self._f16(_VOCALGORITHM_SAMPLING_INTERVAL)
        else:
            if (((sraw > 0) and (sraw < 65000))):
                if ((sraw < 20001)):
                    sraw = 20001
                elif((sraw > 52767)):
                    sraw = 52767
                self.params.msraw = self._fix16_from_int((sraw - 20000))
            self.params.mvoc_index =self._vocalgorithm__mox_model__process(self.params.msraw)
            self.params.mvoc_index =self._vocalgorithm__sigmoid_scaled__process(self.params.mvoc_index)
            self.params.mvoc_index =self._vocalgorithm__adaptive_lowpass__process(self.params.mvoc_index)
            if ((self.params.mvoc_index < self._f16(0.5))):
                self.params.mvoc_index = self._f16(0.5)
            if self.params.msraw > self._f16(0.):
                self._vocalgorithm__mean_variance_estimator__process(self.params.msraw, self.params.mvoc_index)
                self._vocalgorithm__mox_model__set_parameters(self._vocalgorithm__mean_variance_estimator__get_std(),self._vocalgorithm__mean_variance_estimator__get_mean())
        voc_index = self._fix16_cast_to_int((self.params.mvoc_index + self._f16(0.5))) 
        return voc_index
    
    def _vocalgorithm__mean_variance_estimator__init(self):
        self._vocalgorithm__mean_variance_estimator__set_parameters(self._f16(0.),self._f16(0.),self._f16(0.))
        self._vocalgorithm__mean_variance_estimator___init_instances()
    
    def _vocalgorithm__mean_variance_estimator___init_instances(self):
        self._vocalgorithm__mean_variance_estimator___sigmoid__init()
    
    def _vocalgorithm__mean_variance_estimator__set_parameters(self, std_initial, tau_mean_variance_hours, gating_max_duration_minutes):
        self.params.m_mean_variance_estimator_gating_max_duration_minutes = gating_max_duration_minutes
        self.params.m_mean_variance_estimator_initialized = 0
        self.params.m_mean_variance_estimator_mean = self._f16(0.)
        self.params.m_mean_variance_estimator_sraw_offset = self._f16(0.)
        self.params.m_mean_variance_estimator_std = std_initial
        self.params.m_mean_variance_estimator_gamma =self._fix16_div(self._f16((_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *(_VOCALGORITHM_SAMPLING_INTERVAL / 3600.))\
                                                                                  ),(tau_mean_variance_hours +self._f16((_VOCALGORITHM_SAMPLING_INTERVAL / 3600.))))
        self.params.m_mean_variance_estimator_gamma_initial_mean =self._f16(((_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *_VOCALGORITHM_SAMPLING_INTERVAL) \
                                                                                /(_VOCALGORITHM_TAU_INITIAL_MEAN + _VOCALGORITHM_SAMPLING_INTERVAL)))
        self.params.m_mean_variance_estimator_gamma_initial_variance = self._f16(((_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *_VOCALGORITHM_SAMPLING_INTERVAL) \
                                                                                     /(_VOCALGORITHM_TAU_INITIAL_VARIANCE + _VOCALGORITHM_SAMPLING_INTERVAL)))
        self.params.m_mean_variance_estimator_gamma_mean = self._f16(0.)
        self.params.m_mean_variance_estimator__gamma_variance = self._f16(0.)
        self.params.m_mean_variance_estimator_uptime_gamma = self._f16(0.)
        self.params.m_mean_variance_estimator_uptime_gating = self._f16(0.)
        self.params.m_mean_variance_estimator_gating_duration_minutes = self._f16(0.)
    
    def _vocalgorithm__mean_variance_estimator__set_states(self, mean, std, uptime_gamma):
        self.params.m_mean_variance_estimator_mean = mean
        self.params.m_mean_variance_estimator_std = std
        self.params.m_mean_variance_estimator_uptime_gamma = uptime_gamma
        self.params.m_mean_variance_estimator_initialized = True
        
    
    def _vocalgorithm__mean_variance_estimator__get_std(self):
        return self.params.m_mean_variance_estimator_std
    
    def _vocalgorithm__mean_variance_estimator__get_mean(self):
        return (self.params.m_mean_variance_estimator_mean +self.params.m_mean_variance_estimator_sraw_offset)
    
    def _vocalgorithm__mean_variance_estimator___calculate_gamma(self, voc_index_from_prior):
        uptime_limit = self._f16((_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX -_VOCALGORITHM_SAMPLING_INTERVAL))
        if self.params.m_mean_variance_estimator_uptime_gamma < uptime_limit:
            self.params.m_mean_variance_estimator_uptime_gamma =(self.params.m_mean_variance_estimator_uptime_gamma +self._f16(_VOCALGORITHM_SAMPLING_INTERVAL))
        
        if self.params.m_mean_variance_estimator_uptime_gating < uptime_limit:
            self.params.m_mean_variance_estimator_uptime_gating =(self.params.m_mean_variance_estimator_uptime_gating +self._f16(_VOCALGORITHM_SAMPLING_INTERVAL))
        
        self._vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self._f16(1.), self._f16(_VOCALGORITHM_INITI_DURATION_MEAN),self._f16(_VOCALGORITHM_INITI_TRANSITION_MEAN))
        sigmoid_gamma_mean =self._vocalgorithm__mean_variance_estimator___sigmoid__process(self.params.m_mean_variance_estimator_uptime_gamma)
        gamma_mean =(self.params.m_mean_variance_estimator_gamma +(self._fix16_mul((self.params.m_mean_variance_estimator_gamma_initial_mean -self.params.m_mean_variance_estimator_gamma),sigmoid_gamma_mean)))
        gating_threshold_mean =(self._f16(_VOCALGORITHM_GATING_THRESHOLD)\
                                +(self._fix16_mul(self._f16((_VOCALGORITHM_GATING_THRESHOLD_INITIAL -_VOCALGORITHM_GATING_THRESHOLD)),\
                                 self._vocalgorithm__mean_variance_estimator___sigmoid__process(self.params.m_mean_variance_estimator_uptime_gating))))
        self._vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self._f16(1.),gating_threshold_mean,self._f16(_VOCALGORITHM_GATING_THRESHOLD_TRANSITION))
        
        sigmoid_gating_mean =self._vocalgorithm__mean_variance_estimator___sigmoid__process(voc_index_from_prior)
        self.params.m_mean_variance_estimator_gamma_mean =(self._fix16_mul(sigmoid_gating_mean, gamma_mean))
        
        self._vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self._f16(1.), self._f16(_VOCALGORITHM_INITI_DURATION_VARIANCE),self._f16(_VOCALGORITHM_INITI_TRANSITION_VARIANCE))
        
        sigmoid_gamma_variance =self._vocalgorithm__mean_variance_estimator___sigmoid__process( self.params.m_mean_variance_estimator_uptime_gamma)
        
        gamma_variance =(self.params.m_mean_variance_estimator_gamma +\
                        (self._fix16_mul((self.params.m_mean_variance_estimator_gamma_initial_variance \
                                          -self.params.m_mean_variance_estimator_gamma),\
                                          (sigmoid_gamma_variance - sigmoid_gamma_mean))))
        
        gating_threshold_variance =(self._f16(_VOCALGORITHM_GATING_THRESHOLD) \
                                    +(self._fix16_mul(self._f16((_VOCALGORITHM_GATING_THRESHOLD_INITIAL -_VOCALGORITHM_GATING_THRESHOLD)),\
                                     self._vocalgorithm__mean_variance_estimator___sigmoid__process( self.params.m_mean_variance_estimator_uptime_gating))))
        
        self._vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self._f16(1.), gating_threshold_variance,self._f16(_VOCALGORITHM_GATING_THRESHOLD_TRANSITION))
        
        sigmoid_gating_variance =self._vocalgorithm__mean_variance_estimator___sigmoid__process( voc_index_from_prior)
        
        self.params.m_mean_variance_estimator__gamma_variance =(self._fix16_mul(sigmoid_gating_variance, gamma_variance))
        
        self.params.m_mean_variance_estimator_gating_duration_minutes =(self.params.m_mean_variance_estimator_gating_duration_minutes \
                                                                          +(self._fix16_mul(self._f16((_VOCALGORITHM_SAMPLING_INTERVAL / 60.)),\
                                                                                           ((self._fix16_mul((self._f16(1.) - sigmoid_gating_mean),\
                                                                                                             self._f16((1. + _VOCALGORITHM_GATING_MAX_RATIO))))\
                                                                                              -self._f16(_VOCALGORITHM_GATING_MAX_RATIO)))))
        
        if ((self.params.m_mean_variance_estimator_gating_duration_minutes <self._f16(0.))):
            self.params.m_mean_variance_estimator_gating_duration_minutes = self._f16(0.)
        
        if ((self.params.m_mean_variance_estimator_gating_duration_minutes >self.params.m_mean_variance_estimator_gating_max_duration_minutes)):
            self.params.m_mean_variance_estimator_uptime_gating = self._f16(0.)
    
    def _vocalgorithm__mean_variance_estimator__process(self, sraw, voc_index_from_prior):
        if ((self.params.m_mean_variance_estimator_initialized == 0)):
            self.params.m_mean_variance_estimator_initialized = 1
            self.params.m_mean_variance_estimator_sraw_offset = sraw
            self.params.m_mean_variance_estimator_mean = self._f16(0.)
        else:
            if (((self.params.m_mean_variance_estimator_mean >= self._f16(100.)) or (self.params.m_mean_variance_estimator_mean <= self._f16(-100.)))):
                self.params.m_mean_variance_estimator_sraw_offset =(self.params.m_mean_variance_estimator_sraw_offset +self.params.m_mean_variance_estimator_mean)
                self.params.m_mean_variance_estimator_mean = self._f16(0.)
            
            sraw = (sraw - self.params.m_mean_variance_estimator_sraw_offset)
            self._vocalgorithm__mean_variance_estimator___calculate_gamma( voc_index_from_prior)
            delta_sgp = (self._fix16_div((sraw - self.params.m_mean_variance_estimator_mean),self._f16(_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING)))
            if ((delta_sgp < self._f16(0.))):
                c = (self.params.m_mean_variance_estimator_std - delta_sgp)
            else:
                c = (self.params.m_mean_variance_estimator_std + delta_sgp)
            additional_scaling = self._f16(1.)
            if ((c > self._f16(1440.))):
                additional_scaling = self._f16(4.)
            self.params.m_mean_variance_estimator_std = self._fix16_mul(self._fix16_sqrt((self._fix16_mul(additional_scaling,\
                                                                                          (self._f16(_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) -self.params.m_mean_variance_estimator__gamma_variance)))),\
                                                                          self._fix16_sqrt(((self._fix16_mul(self.params.m_mean_variance_estimator_std,\
                                                                                                            (self._fix16_div(self.params.m_mean_variance_estimator_std,\
                                                                                                            (self._fix16_mul(self._f16(_VOCALGORITHM_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING),additional_scaling)))))) \
                                                                                          +(self._fix16_mul((self._fix16_div((self._fix16_mul(self.params.m_mean_variance_estimator__gamma_variance,delta_sgp)),additional_scaling))\
                                                                                          ,delta_sgp)))))
            self.params.m_mean_variance_estimator_mean =(self.params.m_mean_variance_estimator_mean +(self._fix16_mul(self.params.m_mean_variance_estimator_gamma_mean,delta_sgp)))
    
    def _vocalgorithm__mean_variance_estimator___sigmoid__init(self):
        self._vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self._f16(0.), self._f16(0.), self._f16(0.))
    
    def _vocalgorithm__mean_variance_estimator___sigmoid__set_parameters(self, l, x0, k):
        self.params.m_mean_variance_estimator_sigmoid_l = l;
        self.params.m_mean_variance_estimator_sigmoid_k = k;        
        self.params.m_mean_variance_estimator_sigmoid_x0 = x0;        
    
    def _vocalgorithm__mean_variance_estimator___sigmoid__process(self, sample):
        x = (self._fix16_mul(self.params.m_mean_variance_estimator_sigmoid_k,(sample - self.params.m_mean_variance_estimator_sigmoid_x0)))
        if ((x < self._f16(-50.))):
            return self.params.m_mean_variance_estimator_sigmoid_l
        elif ((x > self._f16(50.))):
            return self._f16(0.)
        else:
            return (self._fix16_div(self.params.m_mean_variance_estimator_sigmoid_l,(self._f16(1.) + self._fix16_exp(x))))
    
    def _vocalgorithm__mox_model__init(self):
        self._vocalgorithm__mox_model__set_parameters(self._f16(1.),self._f16(0.))
    
    def _vocalgorithm__mox_model__set_parameters(self,sraw_std,sraw_mean):
        self.params.m_mox_model_sraw_std = sraw_std;
        self.params.m_mox_model_sraw_mean = sraw_mean;        
    
    def _vocalgorithm__mox_model__process(self,sraw):
        return (self._fix16_mul((self._fix16_div((sraw - self.params.m_mox_model_sraw_mean),(-(self.params.m_mox_model_sraw_std +self._f16(_VOCALGORITHM_SRAW_STD_BONUS))))),self._f16(_VOCALGORITHM_VOC_INDEX_GAIN)))
    
    def _vocalgorithm__sigmoid_scaled__init(self):
        self._vocalgorithm__sigmoid_scaled__set_parameters(self._f16(0.))
    
    def _vocalgorithm__sigmoid_scaled__set_parameters(self,offset):
        self.params.m_sigmoid_scaled_offset = offset
    
    def _vocalgorithm__sigmoid_scaled__process(self,sample):
        x = (self._fix16_mul(self._f16(_VOCALGORITHM_SIGMOID_K),(sample - self._f16(_VOCALGORITHM_SIGMOID_X0))))
        if ((x < self._f16(-50.))):
            return self._f16(_VOCALGORITHM_SIGMOID_L)
        elif ((x > self._f16(50.))):
            return self._f16(0.)
        else:
            if ((sample >= self._f16(0.))):
                shift = (self._fix16_div((self._f16(_VOCALGORITHM_SIGMOID_L) -(self._fix16_mul(self._f16(5.), self.params.m_sigmoid_scaled_offset))),self._f16(4.)))
                return ((self._fix16_div((self._f16(_VOCALGORITHM_SIGMOID_L) + shift),(self._f16(1.) + self._fix16_exp(x)))) -shift)
            else:
                return (self._fix16_mul((self._fix16_div(self.params.m_sigmoid_scaled_offset,self._f16(_VOCALGORITHM_VOC_INDEX_OFFSET_DEFAULT))),\
                                         (self._fix16_div(self._f16(_VOCALGORITHM_SIGMOID_L),(self._f16(1.) + self._fix16_exp(x))))))
    
    def _vocalgorithm__adaptive_lowpass__init(self):
        self._vocalgorithm__adaptive_lowpass__set_parameters()
    
    def _vocalgorithm__adaptive_lowpass__set_parameters(self):
        self.params.m_adaptive_lowpass_a1 =self._f16((_VOCALGORITHM_SAMPLING_INTERVAL /(_VOCALGORITHM_LP_TAU_FAST + _VOCALGORITHM_SAMPLING_INTERVAL)))
        self.params.m_adaptive_lowpass_a2 =self._f16((_VOCALGORITHM_SAMPLING_INTERVAL /(_VOCALGORITHM_LP_TAU_SLOW + _VOCALGORITHM_SAMPLING_INTERVAL)))
        self.params.m_adaptive_lowpass_initialized = 0
    
    def _vocalgorithm__adaptive_lowpass__process(self,sample):
        if ((self.params.m_adaptive_lowpass_initialized == 0)):
            self.params.m_adaptive_lowpass_x1 = sample;
            self.params.m_adaptive_lowpass_x2 = sample;
            self.params.m_adaptive_lowpass_x3 = sample;
            self.params.m_adaptive_lowpass_initialized = 1;
        self.params.m_adaptive_lowpass_x1 =((self._fix16_mul((self._f16(1.) - self.params.m_adaptive_lowpass_a1),self.params.m_adaptive_lowpass_x1)) +(self._fix16_mul(self.params.m_adaptive_lowpass_a1, sample)))
        
        self.params.m_adaptive_lowpass_x2 =((self._fix16_mul((self._f16(1.) - self.params.m_adaptive_lowpass_a2),self.params.m_adaptive_lowpass_x2)) +(self._fix16_mul(self.params.m_adaptive_lowpass_a2, sample)))
        
        abs_delta =(self.params.m_adaptive_lowpass_x1 - self.params.m_adaptive_lowpass_x2)
        
        if ((abs_delta < self._f16(0.))):
            abs_delta = (-abs_delta)
        F1 = self._fix16_exp((self._fix16_mul(self._f16(_VOCALGORITHM_LP_ALPHA), abs_delta)))
        tau_a =((self._fix16_mul(self._f16((_VOCALGORITHM_LP_TAU_SLOW - _VOCALGORITHM_LP_TAU_FAST)),F1)) +self._f16(_VOCALGORITHM_LP_TAU_FAST))
        a3 = (self._fix16_div(self._f16(_VOCALGORITHM_SAMPLING_INTERVAL),(self._f16(_VOCALGORITHM_SAMPLING_INTERVAL) + tau_a)))
        self.params.m_adaptive_lowpass_x3 =((self._fix16_mul((self._f16(1.) - a3), self.params.m_adaptive_lowpass_x3)) +(self._fix16_mul(a3, sample)))
        return self.params.m_adaptive_lowpass_x3


# ----------------------------------------------------------------------
# SGP40 driver

_DEFAULT_NAME = "Qwiic SGP40"

_AVAILABLE_I2C_ADDRESS = [0x59]

class QwiicSGP40(object):
    """!
    QwiicSGP40

    @param address: The I2C address to use for the device.
                        If not provided, the default address is used.
    @param i2c_bus: A qwiic_i2c bus or a native bus object. If not provided, the default bus is used.

    @return **Object** The GPIO device object.
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
  
    # SGP40 I2C commands
    SGP40_MEASURE_RAW = [0x26, 0x0F]
    SGP40_MEASURE_TEST = [0x28, 0x0E]
    SGP40_HEATER_OFF = [0x36, 0x15]
    SGP40_SOFT_RESET = [0x00, 0x06]
  
    # SGP40 Measure Test Results
    SGP40_MEASURE_TEST_PASS = [0xD4, 0x00]
    SGP40_MEASURE_TEST_FAIL = [0x4B, 0x00]
  
    DURATION_WAIT_MEASURE_TEST = 0.32
    DURATION_READ_RAW_VOC = 0.03
  
    # Constructor
    def __init__(self, address=None, i2c_bus=None):
    
        # The bus may come first: QwiicDevice(bus) or QwiicDevice(bus, 0x76)
        address, i2c_bus = qwiic_i2c.device_args(address, i2c_bus)
        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]
    
        # Use the given I2C bus, or the platform's default bus
        self._i2c = qwiic_i2c.get_i2c_bus(i2c_bus)
                
        self.__my_vocalgorithm = _DFRobotVOCAlgorithm()
        self.__rh = 0
        self.__temc = 0
        self.__rh_h = 0
        self.__rh_l = 0
        self.__temc_h = 0
        self.__temc_l = 0
        self.__temc__crc = 0
        self.__rh__crc = 0

    # --------------------------------------------------------------------
    # is_connected()
    #
    # Is an actual board connected to our sysem?
    def is_connected(self):
        """!
        Determine if a Qwiic SGP40 device is connected to the system.

        @return **bool** True if the device is connected, false otherwise.
        """
        return self._i2c.is_device_connected(self.address)

    # --------------------------------------------------------------------
    # begin()
    # 
    # Initialize I2C communication and wait through warm-up time.
    def begin(self, warm_up_time = 10):
        """!
        Initialize the operation of the Qwiic SGP40 and wait through warm-
            up time. Run is_connected() and measure_test().

        @param warm_up_time: Seconds to spend reading the sensor before the self test

        @return **bool** Returns True if the device is connected and passed its self test, otherwise False.
        """
        if self.is_connected():
            
            self.__my_vocalgorithm.vocalgorithm_init()
            start_time = self._i2c.ticks_ms()
            while self._i2c.ticks_diff(self._i2c.ticks_ms(), start_time) < warm_up_time * 1000:
                self.get_voc_index()
            return self.measure_test() == 0
        
        return False

    # --------------------------------------------------------------------
    # measure_test()
    #
    # Sensor runs chip self test
    def measure_test(self):
        """!
        Sensor runs chip self test.

        @return **int** Returns 0 if the self-test succeeded and 1 if it failed.
        """
        temp0 = self.SGP40_MEASURE_TEST[0]
        temp1 = self.SGP40_MEASURE_TEST[1]
        
        self._i2c.write_byte(self.address, temp0, temp1)
        self._i2c.delay_ms(self.DURATION_WAIT_MEASURE_TEST * 1000)
        # The result is read directly, with no register or command first
        result = self._i2c.read_block(self.address, None, 3)
        
        if result[0] == self.SGP40_MEASURE_TEST_PASS[0] and result[1] == self.SGP40_MEASURE_TEST_PASS[1]:
            return 0
        else:
            return 1

    # --------------------------------------------------------------------
    # soft_reset()
    #
    # Performs a soft reset
    def soft_reset(self, ignore_error = True):
        """!
        Sensor reset

        @param ignore_error: **bool, optional** Whether to ignore exception that can be raised
            due to no ACK after reset command, defaults to True
        """
        temp0 = self.SGP40_SOFT_RESET[0]
        temp1 = self.SGP40_SOFT_RESET[1]

        # Attempt to reset the sensor. The SGP40 does not send back an ACK, so
        # an error is expected. If ignore_error is False, the error is raised.
        try:
            self._i2c.write_byte(self.address, temp0, temp1)
        except OSError:
            if not ignore_error:
                raise

    # --------------------------------------------------------------------
    # heater_off()
    #
    # Turns the heater off
    def heater_off(self):
        """!
        Turns the hotplate off and puts sensor in idle mode.
        """
        temp0 = self.SGP40_HEATER_OFF[0]
        temp1 = self.SGP40_HEATER_OFF[1]
        self._i2c.write_byte(self.address, temp0, temp1)

    # --------------------------------------------------------------------
    # measure_raw(relative_humidity, temperature_c)
    #
    # The raw signal is returned in SRAW_ticks. The user can provide relative
    # humidity or temperature parameters if desired.
    def measure_raw(self, relative_humidity = 50, temperature_c = 25):
        """!
        Returns the raw data. See the SGP40 datasheet for more info.

        @param relative_humidity: float relative humidity between 0 and 100%.
        @param temperature_c: float temperature in celcius between -45 and 130 degrees.

        @return **int** The raw signal in SRAW ticks if the CRC checks out, -1 otherwise
        """
        # Check boundaries of relative humidity and temperature
        if relative_humidity < 0:
            relative_humidity = 0
        if relative_humidity > 100:
            relative_humidity = 100
        if temperature_c < -45:
            temperature_c = -45
        if temperature_c > 130:
            temperature_c = 130

        
        # Calculate relative humidity and temperature ticks
        self.__rh = int(((relative_humidity*65535)/100+0.5))
        self.__temc = int(((temperature_c+45)*(65535/175)+0.5))
        # Break it into bytes and calculate CRC
        self.__rh_h = int(self.__rh)>>8
        self.__rh_l = int(self.__rh)&0xFF
        self.__rh__crc = self.__crc(self.__rh_h, self.__rh_l)
        self.__temc_h = int(self.__temc)>>8
        self.__temc_l = int(self.__temc)&0xFF
        self.__temc__crc = self.__crc(self.__temc_h, self.__temc_l)
        
        temp0 = int(self.SGP40_MEASURE_RAW[0])
        temp1 = int(self.SGP40_MEASURE_RAW[1])
        write_bytes = [temp1, int(self.__rh_h), int(self.__rh_l), int(self.__rh__crc), int(self.__temc_h), int(self.__temc_l), int(self.__temc__crc)]
        
        self._i2c.write_block(self.address, temp0, write_bytes)

        self._i2c.delay_ms(self.DURATION_READ_RAW_VOC * 1000)
        
        # Data is read back in 3 bytes: data (MSB) / data (LSB) / Cecksum
        # The result is read directly, with no register or command first
        result = self._i2c.read_block(self.address, None, 3)
        
        if self.__check_crc(result) == 0:
            return result[0]<<8 | result[1]
        else:
            return -1
    
    # --------------------------------------------------------------------
    # __check__crc(raw)
    #
    # Verify the calibration value of the sensor
    def __check_crc(self, raw):
        """!
        Verify the calibration value of the sensor

        @param raw: list parameter to check

        @return **int** -1 if the check failed, 0 if it succeeded
        """
        assert (len(raw) == 3)
        if self.__crc(raw[0], raw[1]) != raw[2]:
            return -1
        return 0
    
    # --------------------------------------------------------------------
    # __crc(data_1, data_2)
    #
    # CRC calculation
    def __crc(self, data_1, data_2):
        """!
        CRC calculation

        @param data_1: high 8 bits of data
        @param data_2: low 8 bits of data

        @return **int** calibration value
        """
        crc = 0xff
        list = [data_1, data_2]
        for i in range(0, 2):
            crc = crc ^ list[i]
            for bit in range(0, 8):
                if (crc & 0x80):
                    crc = ((crc << 1) ^ 0x31)
                else:
                    crc = (crc << 1)
            
            # TODO: not sure if this line is necessary.
            # It is not in the datasheet sample code pg 12
            crc = crc & 0xFF
        return crc
            
    # --------------------------------------------------------------------
    # get_voc_index(relative_humidity, temperature_c)
    #
    # Get VOC index
    def get_voc_index(self, relative_humidity = 50, temperature_c = 25):
        """!
        Get VOC index

        @param relative_humidity: float relative humidity between 0 and 100%.
        @param temperature_c: float temperature in celcius between -45 and 130 degrees.

        @return **int** VOC index
        """
        raw = self.measure_raw(relative_humidity, temperature_c)

        if raw < 0:
            return -1
        else:
            voc_index = self.__my_vocalgorithm.vocalgorithm_process(raw)
            return voc_index

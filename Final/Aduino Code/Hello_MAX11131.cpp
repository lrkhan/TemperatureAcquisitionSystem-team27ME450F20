// /*******************************************************************************
// * Copyright (C) 2019 Maxim Integrated Products, Inc., All Rights Reserved.
// *
// * Permission is hereby granted, free of charge, to any person obtaining a
// * copy of this software and associated documentation files (the "Software"),
// * to deal in the Software without restriction, including without limitation
// * the rights to use, copy, modify, merge, publish, distribute, sublicense,
// * and/or sell copies of the Software, and to permit persons to whom the
// * Software is furnished to do so, subject to the following conditions:
// *
// * The above copyright notice and this permission notice shall be included
// * in all copies or substantial portions of the Software.
// *
// * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// * IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
// * OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
// * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// * OTHER DEALINGS IN THE SOFTWARE.
// *
// * Except as contained in this notice, the name of Maxim Integrated
// * Products, Inc. shall not be used except as stated in the Maxim Integrated
// * Products, Inc. Branding Policy.
// *
// * The mere transfer of this software does not imply any licenses
// * of trade secrets, proprietary technology, copyrights, patents,
// * trademarks, maskwork rights, or any other form of intellectual
// * property whatsoever. Maxim Integrated Products, Inc. retains all
// * ownership rights.
// *******************************************************************************
// */
// example code includes
// standard include for target platform -- Platform_Include_Boilerplate
#include "Arduino.h"
// SPI interface
#include "SPI.h"
// end Platform_Include_Boilerplate
#include "MAX11131.h"
// math
#include <math.h>
#include  <time.h>

// LK -  this is the chip select for the SPI
// example code declare SPI interface
// global SPI uses conventional Arduino 10-pin header D11 D12 D13
// chip select is on Arduino 10-pin header D10
uint8_t spi_cs = 10; // Generic: Arduino 10-pin header D10

// example code declare GPIO interface pins
uint8_t CNVST_pin = 9; // Digital Trigger Input to MAX11131 device
// uint8_t REF_plus_pin = Px_x_PortName_To_Be_Determined; // Reference Input to MAX11131 device
// uint8_t REF_minus_slash_AIN15_pin = Px_x_PortName_To_Be_Determined; // Reference Input to MAX11131 device
uint8_t EOC_pin = 2; // Digital Event Output from MAX11131 device
// example code declare device instance
MAX11131 g_MAX11131_device(spi_cs, CNVST_pin, EOC_pin, MAX11131::MAX11131_IC);

double temp(double voltage, int chan){
  if (voltage == 0){
    return 0;
    }
  
  int rL[] = {991, 994, 989, 998, 996, 993, 1002, 987, 984, 996};
  double vRef = 3.3;

  double r = (voltage * rL[chan])/ (vRef - voltage);
  
  double tempreature = 0;

  // steinheart constants
  double A = 0.02324341278;
  double B = -0.003600335913;
  double C = 0.00001511095903;

  // temp calcs
  tempreature = A + (B * log(r)) + (C * pow((log(r)), 3));
  tempreature = 1/tempreature;
  tempreature = tempreature - 273.15;
  
  if (tempreature <= 0){
    return 0;
    }
  
  return tempreature;
  }

// example code main function
int main()
{
    // example code: serial port banner message
    Serial.begin(1200); // serial baud rate
    
    g_MAX11131_device.Init();
  
    while(1) { // this code repeats forever
        // this code repeats forever
        // Measure ADC channels in sequence from AIN0 to channelNumber_0_15.
        // @param[in] g_MAX11131_device.channelNumber_0_15: AIN Channel Number
        // @param[in] g_MAX11131_device.PowerManagement_0_2: 0=Normal, 1=AutoShutdown, 2=AutoStandby
        // @param[in] g_MAX11131_device.chan_id_0_1: ADC_MODE_CONTROL.CHAN_ID
        int channelId_0_15 = 9;
        g_MAX11131_device.channelNumber_0_15 = channelId_0_15;
        g_MAX11131_device.PowerManagement_0_2 = 0;
        g_MAX11131_device.chan_id_0_1 = 1;
        g_MAX11131_device.NumWords = g_MAX11131_device.ScanStandardExternalClock();

        // Read raw ADC codes from device into AINcode[] and RAW_misoData16[]
        // @pre one of the MAX11311_Scan functions was called, setting g_MAX11131_device.NumWords
        g_MAX11131_device.ReadAINcode();
        // @post RAW_misoData16[index] contains the raw SPI Master-In,Slave-Out data
        // @post AINcode[NUM_CHANNELS] contains the latest readings in LSBs

        //wait(1.0);
        // Use Arduino Serial Plotter to view output: Tools | Serial Plotter
        int adcVal = g_MAX11131_device.AINcode[0];
        
        double voltage = (3.3 * adcVal) / (4095);
        //Serial.print(adcVal);
        Serial.print(temp(voltage, 0));
        
        // Serial.print(g_MAX11131_device.AINcode[0]);
        
        for (int index = 1; index <= channelId_0_15; index++) {
            Serial.print(",");
            adcVal = g_MAX11131_device.AINcode[index];
            voltage = (3.3 * adcVal) / (4095);
            //Serial.print(adcVal);
            Serial.print(temp(voltage, index));
            // Serial.print(g_MAX11131_device.AINcode[index]);
        }
        Serial.println();
    } // this code repeats forever
}

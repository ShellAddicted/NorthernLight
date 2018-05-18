/*
	Copyright (c) 2018
	
	Gaspare Caterino <shelladdicted@gmail.com>
		github.com/ShellAddicted
	
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "Arduino.h"

#define ADC_PIN A0
#define ADC_RES 10

uint64_t adcScale = 0;
uint8_t data[2] = {0};

void setup() {
	adcScale = pow(2,ADC_RES);
	Serial.begin(115200,SERIAL_8N1);
}

void loop() {
	uint64_t adcValue = analogRead(ADC_PIN);
	data[0] = 0xFB; // Control Code -> OK
	data[1] = (adcValue/(double)adcScale)*100; // ADC value as %
	Serial.write(data,2);
	delay(1);
}
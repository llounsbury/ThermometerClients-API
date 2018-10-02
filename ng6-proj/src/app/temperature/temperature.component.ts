import {Component, Input, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';
import {FormsModule} from '@angular/forms';
import {NgModule} from '@angular/core';
import { AppComponent } from 'src/app/app.component';
import {log} from 'util';
import {text} from '@angular/core/src/render3/instructions';





@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.scss']
})



export class TemperatureComponent {
    APIHOST: String = 'http://0.0.0.0:5000/';
    temperature: String = '';
    temperatureF: String = '';
    tempFormat: String = '0';
    LED: String = '0';
    min = '';
    minInput = 'Enter New Min';
    max = '';
    maxInput = 'Enter New Max';
    upluggedNotification = 'Unplugged Sensor';
    offNotification = 'No Data Available';
    cellNumber = '5555555555';
    cellNumberInput = 'Update Phone Number';
    cellCarrier = '';
    cellCarrierInput = 'Update Cell Carrier';
    carriers: any[] = [
        {
            'name': 'verizon'
        },
        {
            'name': 'at&t'
        },
        {
            'name': 'sprint'
        },
        {
            'name': 't-mobile'
        }
    ];

    updateCellCarrier(newCarrier) {
        let http_url: string;
        http_url = this.APIHOST + 'carrier/' + newCarrier;
        this.http.post(http_url, null).subscribe();
    }

    updateCellNumber() {
        let http_url: string;
        http_url = this.APIHOST + 'cell/' + this.cellNumberInput;
        this.http.post(http_url, null).subscribe();
    }

    tempFormatChange() {
      if (this.tempFormat === '1') {
        this.tempFormat = '0';
      } else {
        this.tempFormat = '1';
      }
    }

    updateTemperature() {
        this.http.get(this.APIHOST + 'temp').subscribe(res => {
            if (res.toString() === '404') {
                this.temperature = this.upluggedNotification;
                this.temperatureF = this.upluggedNotification;
            } else if (res.toString() === '405') {
              this.temperature = this.offNotification;
              this.temperatureF = this.offNotification;
            } else {
                this.temperature = (res).toString();
                this.temperatureF = (Number(this.temperature) * 1.8 + 32).toFixed(2).toString();
            }
        });
    }

    update_led() {
        this.http.post(this.APIHOST + 'led', null).subscribe(res => {
            this.LED = (res).toString();
        });
    }

    update_min() {
      let http_url: string;
      http_url = this.APIHOST + 'min/' + this.minInput.toString();
        this.http.post(http_url, null).subscribe();
    }

    update_max() {
        let http_url: string;
        http_url = this.APIHOST + 'max/' + this.maxInput.toString();
        this.http.post(http_url, null).subscribe();
    }

  constructor(private http: HttpClient) {
      this.http.get(this.APIHOST + 'led').subscribe(res => {
          this.LED = (res).toString();
      });
      this.updateTemperature();
      this.http.get(this.APIHOST + 'led').subscribe(res => {
          this.LED = (res).toString();
      });
      this.http.get(this.APIHOST + 'min').subscribe(res => {
          this.min = (res).toString();
      });
      this.http.get(this.APIHOST + 'max').subscribe(res => {
          this.max = (res).toString();
      });
      setInterval(() => {
              this.updateTemperature();
              this.http.get(this.APIHOST + 'carrier').subscribe(res => {
                  this.cellCarrier = ( (JSON.parse(JSON.stringify(res)))['name']);
              });
              this.http.get(this.APIHOST + 'cell').subscribe(res => {
                  this.cellNumber = (res).toString();
              });
              this.http.get(this.APIHOST + 'led').subscribe(res => {
                  this.LED = (res).toString();
              });
              this.http.get(this.APIHOST + 'min').subscribe(res => {
                  this.min = (res).toString();
              });
              this.http.get(this.APIHOST + '/max').subscribe(res => {
                  this.max = res.toString();
              });
          }
          , 1000);
  }
}


import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import * as Chartist from 'chartist';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  myControl = new FormControl();
  options: string[] = [];
  

  constructor(private api: ApiService) { }
 
  
  ngOnInit() {
  }

  /*
  getOPtions() {
    this.api.getEvents()
      .subscribe(data => {
        if ('teams' in data){
          
        }
        
      });
      
  }*/

}

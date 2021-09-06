import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import * as Chartist from 'chartist';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  myControl = new FormControl();
  options: string[] = ['One', 'Two', 'Three'];

  constructor() { }
 
  
  ngOnInit() {
  }

}

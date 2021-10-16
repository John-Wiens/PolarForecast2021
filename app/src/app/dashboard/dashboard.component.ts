import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';
import * as Chartist from 'chartist';
import { ApiService } from '../services/api.service';
import {map, startWith} from 'rxjs/operators';
import {Observable} from 'rxjs';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  myControl = new FormControl();
  options: string[] = [];
  filteredOptions: Observable<string[]>;
  data: any = [];
  constructor(private api: ApiService) { }
 
  
  ngOnInit() {
    console.log('test');
    this.getOptions(); 
  }

  onSelectionChanged(event: MatAutocompleteSelectedEvent) {
    for(let i=0; i < this.data.length; i++){
      if(event.option.value == this.data[i]['name']){
        this.setEvent(this.data[i]['name'],this.data[i]['key']);
        break
      }
    }
  }
  setEvent(eventName, event){
    localStorage.setItem('eventName', eventName);
    localStorage.setItem('event', event);
  }

  
  getOptions() {
    this.api.getEvents()
      .subscribe(data => {
        if('data' in data){

          this.data = data['data'];
          console.log(this.data);
          for(let i =0; i < data['data'].length;i++){
            this.addOption('name',data['data'][i]);
          }
        }
        this.filteredOptions = this.myControl.valueChanges.pipe(
          startWith(''),
          map(value => this._filter(value))
        );
      });
  }

  addOption(key, source){
    if ('key' in source){
      this.options.push(source[key]);
    }
  }



  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

}

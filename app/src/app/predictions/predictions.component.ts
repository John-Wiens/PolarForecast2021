import { Component, OnInit, Pipe, ViewChild, HostListener} from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort } from '@angular/material/sort';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-predictions',
  templateUrl: './predictions.component.html',
  styleUrls: ['./predictions.component.css']
})
export class PredictionsComponent implements OnInit {

  displayedColumns: string[] = ['rank','key','max', 'min', 'average'];

  dataSource = null;

  data: any = [];

  @ViewChild('sort') sort: MatSort;

  public innerWidth: any;

  ngOnInit() {
    this.getPredictedRankings();
    this.data.sort = this.sort;
    this.innerWidth = window.innerWidth;
  }


  @HostListener('window:resize', ['$event'])
    onResize(event) {
    this.innerWidth = window.innerWidth;
  }

  getResponsiveMode(){
    return this.innerWidth < 640;
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  constructor(private api: ApiService) { }

  getPredictedRankings(){
    const event = this.getEvent();
    if(event!= null){
      this.api.getPredictedRankings(event)
      .subscribe(data => {
        if ('rankings' in data){
          this.data = data['rankings'];
          this.data.sort(function(first, second) {
            return second.rank - first.rank;
           });
          this.dataSource = new MatTableDataSource(this.data);
          
          this.dataSource.sort = this.sort;
          console.log(this.data);
        }
      });
    }
  }

  getEvent(){
    const event = localStorage.getItem('event');
    if(event == null){
        return ""
    } else{
        return event;
    }
  }
}

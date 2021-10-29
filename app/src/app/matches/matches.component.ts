import { Component, OnInit, Pipe, ViewChild, HostListener} from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort } from '@angular/material/sort';
import { ApiService } from '../services/api.service';


@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.css']
})
export class MatchesComponent implements OnInit {

  displayedColumns: string[] = ['match_number','blue_score', 'blue_rp', 'red_score', 'red_rp','results'];
  dataSource = null;
  finalsDataSource = null;

  data: any = [];//this.ELEMENT_DATA;
  finalsData: any = [];

  elims = true;

  @ViewChild('sort') sort: MatSort;
  @ViewChild('finalsSort') finalsSort: MatSort;

  public innerWidth: any;

  ngOnInit() {
    this.getMatches();
    this.data.sort = this.sort;
    this.finalsData.sort = this.finalsSort;
    this.innerWidth = window.innerWidth;
  }


  @HostListener('window:resize', ['$event'])
    onResize(event) {
    this.innerWidth = window.innerWidth;
  }

  getResponsiveMode(){
    return this.innerWidth < 640;
  }

  //dataSource = null;//new MatTableDataSource(this.data);


  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    //this.finalsDataSource.sort = this.sort;
  }

  constructor(private api: ApiService) { }

  getMatches() {
    const event = localStorage.getItem('event');
    if(event!= null){
      this.api.getMatches(event,'qm')
      .subscribe(data => {
        if ('data' in data){
          this.data = data['data'];
          this.data.sort(function(first, second) {
            return first.match_number - second.match_number;
           });
          this.dataSource = new MatTableDataSource(this.data);
          this.dataSource.sort = this.sort;
          this.elims = true;
          for (const [key, value] of Object.entries(this.data)) {
            console.log(key, value);
            if(value['results'] != 'Actual'){
              this.elims = false;
            }
          }
          if(this.elims){
            this.getFinalsMatches();
          }
        }
      });
    }
  }

  getFinalsMatches(){
    const event = localStorage.getItem('event');
    if(event!= null){
      this.api.getMatches(event,'elim')
      .subscribe(data => {
        if ('data' in data){
          this.finalsData = data['data'];
          
          for(let i=0; i < this.finalsData.length;i++){
            let entry = this.finalsData[i];
            let comp_level = entry['comp_level']
            if(comp_level == 'f'){
              entry['match_order'] = 100 + entry['set_number'];
            }else if(comp_level == 'sf'){
              entry['match_order'] = 10 + entry['set_number'];
            } else if(comp_level == 'qf'){
              entry['match_order'] = entry['set_number'];
            }
          }
          this.finalsData.sort(function(first, second) {
            return first.match_order - second.match_order;
           });

          console.log(this.finalsData);
          this.finalsDataSource = new MatTableDataSource(this.finalsData);
          this.finalsDataSource.sort = this.finalsSort;
        }
      });
    }
  }

  getWinner(match){
    if(match['blue_score'] > match['red_score']){
      return 'Blue'
    } else{
      return 'Red'
    } 
  }

  getWinnerPoints(match){
    if(match['blue_score'] > match['red_score']){
      return Math.round(match['blue_score'])
    } else{
      return Math.round(match['red_score'])
    }
  }
}

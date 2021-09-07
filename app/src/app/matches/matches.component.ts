import { Component, OnInit, Pipe, ViewChild} from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort } from '@angular/material/sort';
import { ApiService } from '../services/api.service';


export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.css']
})
export class MatchesComponent implements OnInit {

  displayedColumns: string[] = ['match_number','blue_score', 'blue_rp', 'red_score', 'red_rp','results'];
  //columnHeaders = ['Rank', 'Team', 'OPR', 'Auto','Control','Endgame','Cells','BPM','Fouls','Power'].slice();
 // columnsToDisplay: string[] = this.displayedColumns.slice();
  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];

  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];
  dataSource = null;

  data: any = [];//this.ELEMENT_DATA;

  @ViewChild(MatSort) sort: MatSort;


  ngOnInit() {
    this.getMatches();
    //this.data.sort = this.sort;
  }

  //dataSource = null;//new MatTableDataSource(this.data);


  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  

  constructor(private api: ApiService) { }

  getMatches() {
    const event = localStorage.getItem('event');
    if(event!= null){
      this.api.getMatches(event,'qm')
      .subscribe(data => {
        if ('data' in data){
          this.data = data['data'];
          console.log(this.data);
          this.dataSource = new MatTableDataSource(this.data);
          this.dataSource.sort = this.sort;
        }
      });
    
    }
  }
}

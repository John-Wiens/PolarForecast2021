import { Component, OnInit, Pipe, ViewChild} from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort } from '@angular/material/sort';
import { ApiService } from '../services/api.service';


@Pipe({name: 'round'})
export class RoundPipe {
  transform (input:number) {
    return Math.round(input*100)/100.0;
  }
}


export interface Element {
  position: number,
  name: string,
  weight: number,
  symbol: string
}



@Component({
  selector: 'app-rankings',
  templateUrl: './rankings.component.html',
  styleUrls: ['./rankings.component.css']
})
export class RankingsComponent implements OnInit {

  displayedColumns: string[] = ['rank', 'team', 'opr', 'auto','control','endgame','cells','bpm','fouls','power'];
  columnHeaders = ['Rank', 'Team', 'OPR', 'Auto','Control','Endgame','Cells','BPM','Fouls','Power'].slice();
  columnsToDisplay: string[] = this.displayedColumns.slice();
  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];

  data: any = [];//this.ELEMENT_DATA;

  @ViewChild(MatSort) sort: MatSort;


  ngOnInit() {
    this.getRankings();
    this.data.sort = this.sort;
  }

  

  constructor(private api: ApiService) { }

  getRankings() {
    const event = this.getEvent();
    if(event!= null){
      this.api.getRankings(event)
      .subscribe(data => {
        if ('rankings' in data){
          this.data = data['rankings'];
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

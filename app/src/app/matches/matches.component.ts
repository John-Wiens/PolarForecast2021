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


  
  ELEMENT_DATA: PeriodicElement[] = [
    {position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H'},
    {position: 2, name: 'Helium', weight: 4.0026, symbol: 'He'},
    {position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li'},
    {position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be'},
    {position: 5, name: 'Boron', weight: 10.811, symbol: 'B'},
    {position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C'},
    {position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N'},
    {position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O'},
    {position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F'},
    {position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne'},
  ];

  displayedColumns: string[] = ['match_number','blue_score', 'blue_rp', 'red_score', 'red_rp','results'];
  //columnHeaders = ['Rank', 'Team', 'OPR', 'Auto','Control','Endgame','Cells','BPM','Fouls','Power'].slice();
 // columnsToDisplay: string[] = this.displayedColumns.slice();
  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];

  //displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];
  dataSource = new MatTableDataSource(this.ELEMENT_DATA);

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

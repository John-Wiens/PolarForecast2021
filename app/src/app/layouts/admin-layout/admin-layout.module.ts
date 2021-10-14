import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AdminLayoutRoutes } from './admin-layout.routing';
import { DashboardComponent } from '../../dashboard/dashboard.component';
import { RankingsComponent } from '../../rankings/rankings.component';
import { MatchesComponent } from '../../matches/matches.component';
import { TeamsComponent } from '../../teams/teams.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { IconsComponent } from '../../icons/icons.component';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatRippleModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTooltipModule }  from '@angular/material/tooltip';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule } from '@angular/material/sort';
import { MatAutocompleteModule} from '@angular/material/autocomplete';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCardModule } from '@angular/material/card';
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatRippleModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTooltipModule,
    MatTableModule,
    CdkTableModule,
    MatSortModule,
    MatAutocompleteModule,
    MatExpansionModule,
    MatCardModule,
  ],
  declarations: [
    DashboardComponent,
    TableListComponent,
    IconsComponent,
    RankingsComponent,
    MatchesComponent,
    TeamsComponent,
  ]
})

export class AdminLayoutModule {}

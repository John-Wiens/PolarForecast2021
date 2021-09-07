import { Routes } from '@angular/router';

import { DashboardComponent } from '../../dashboard/dashboard.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { IconsComponent } from '../../icons/icons.component';
import { RankingsComponent } from '../../rankings/rankings.component';
import { MatchesComponent } from '../../matches/matches.component';
import { TeamsComponent } from 'app/teams/teams.component';

export const AdminLayoutRoutes: Routes = [
    { path: 'dashboard',      component: DashboardComponent },
    { path: 'table-list',     component: TableListComponent },
    { path: 'icons',          component: IconsComponent },
    { path: 'rankings',        component: RankingsComponent },
    { path: 'matches',        component: MatchesComponent },
    { path: 'teams',        component: TeamsComponent },
];

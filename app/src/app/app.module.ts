import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { MatTableModule} from '@angular/material/table';
import { AppRoutingModule } from './app.routing';
import { ComponentsModule } from './components/components.module';
import { AppComponent } from './app.component';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort} from '@angular/material/sort';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import { RoundPipe } from './round.pipe';

@NgModule({
  imports: [
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ComponentsModule,
    RouterModule,
    AppRoutingModule,
    MatTableModule,
    CdkTableModule,
    MatSortModule,
    MatAutocompleteModule,
    //MatSort
  ],
  declarations: [
    AppComponent,
    AdminLayoutComponent,
    RoundPipe,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

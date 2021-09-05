import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost:8000'
  constructor(private http: HttpClient) { }

  getRankings(event_key) {
    return this.http.get(this.API_URL + '/events/'+ event_key+'/rankings');
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AppConfig } from '../../app.config';


@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) {}

  getProfileInfo(): Observable<any> {
    return this.http.get<any>(
      `${AppConfig.serverUrl}/api/my_profile`,
      {
        headers: {
          'Authorization': 'bearer ' + AppConfig.bearerToken
        }
      }
    );
  }

  getQuizResults(): Observable<any> {
    return this.http.get<any>(
      `${AppConfig.serverUrl}/api/quiz_results`,
      {
        headers: {
          'Authorization': 'bearer ' + AppConfig.bearerToken
        }
      }
    );
  }

}

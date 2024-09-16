import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AppConfig } from '../app.config';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) {}

  signIn(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post<any>(
      `${AppConfig.serverUrl}/sign_in`,
      null,
      {
        params: {
          username: username,
          password: password
        }
      }
    );
  }
}

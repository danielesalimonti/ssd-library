import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../environments/environment';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  getToken(){
    return localStorage.getItem('token');
  }

  isLogged(){ return this.getToken() !== '';}

  login(username, password){
    return this.http.post(environment.backend_url+'/auth/login/', {username, password})
      .pipe(
        map( (result: any) => {
          localStorage.setItem('token', result.key);
          return true;
        })
      );
  }

  logout(){
    return this.http.post(environment.backend_url+'/auth/logout/', {}).pipe(
      map( value => {
        localStorage.removeItem('token');
        return value;
      })
    );
  }

  register(username, email, password){
    return this.http.post(environment.backend_url+'/auth/registration/', {username, email, password1: password, password2: password})
      .pipe(
        map( (result: any) => {
          localStorage.setItem('token', result.key);
          return true;
        })
      );
  }
}

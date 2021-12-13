import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Book} from '../app/model/book';
import {environment} from '../environments/environment';
import {AuthService} from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  constructor(private http: HttpClient,
              private auth: AuthService) { }

  getAllBooks(){
    return this.http.get<Book[]>(environment.backend_url+'/', this.getHeader());
  }

  getMyBooks(){
    return this.http.get<Book[]>(environment.backend_url+'/my-books/', this.getHeader());
  }

  showBook(isbn){
    return this.http.get<Book>(environment.backend_url+'/my-books/'+isbn, this.getHeader());
  }

  rentBook(isbn){
    return this.http.get(environment.backend_url+'/rent/'+isbn, this.getHeader());
  }

  getHeader() {
    return {headers: {'Authorization': 'Token ' + this.auth.getToken()}};
  }

}

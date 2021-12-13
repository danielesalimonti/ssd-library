import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Book} from '../app/model/book';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  constructor(private http: HttpClient) { }

  getBooks(){
    return this.http.get<Book[]>('http://localhost:8000/api/v1/books/');
  }
}

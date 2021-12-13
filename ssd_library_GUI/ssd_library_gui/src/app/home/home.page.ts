import { Component } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {BookService} from '../../services/book.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  loading = true;
  books: Book[] = [];

  constructor(public router: Router, private bookService: BookService) {


    bookService.getBooks().subscribe( (data) =>{
      this.books = data;
      this.loading = false;
    });
  }
}

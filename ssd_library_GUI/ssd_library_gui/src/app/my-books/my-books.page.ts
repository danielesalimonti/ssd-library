import { Component, OnInit } from '@angular/core';
import {Book} from "../model/book";
import {Router} from "@angular/router";

@Component({
  selector: 'app-my-books',
  templateUrl: './my-books.page.html',
  styleUrls: ['./my-books.page.scss'],
})
export class MyBooksPage implements OnInit {

  myBooks: Book[] = [];

  constructor(public router: Router) {
    this.myBooks.push(new Book('321312312', 'Tiziano Sclavi', 'MIO LIBRO', 'libro', 'An horror book...',
      new Date(), 125
    ));
  }

  goToMyBook(isbn: string) {
    this.router.navigate(['/book', isbn]);
  }

  ngOnInit() {
  }

}

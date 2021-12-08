import { Component } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  books: Book[] = [];

  constructor(public router: Router) {

    this.books.push(new Book('321312312', 'Tiziano Sclavi', 'Nero', 'libro', 'An horror book...',
      new Date(), 125
    ),
      new Book('32131sda2', 'ALtro Autore', 'Boh', 'libro', 'A comic book...',
        new Date(), 138)
    );
  }
}

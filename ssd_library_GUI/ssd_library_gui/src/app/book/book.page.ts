import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-book',
  templateUrl: './book.page.html',
  styleUrls: ['./book.page.scss'],
})
export class BookPage implements OnInit {

  book: Book;

  constructor(public activatedRoute: ActivatedRoute, public router: Router) {
    const isbn = this.activatedRoute.snapshot.params['isbn'];
    console.log(isbn);
    // eslint-disable-next-line max-len
    this.book = new Book(isbn, 'Tiziano Sclavi', 'Nero', 'libro', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
      new Date(), 125
    );
  }

  ngOnInit() {
  }

}

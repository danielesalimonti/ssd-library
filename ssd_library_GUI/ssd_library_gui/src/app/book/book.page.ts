import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';

@Component({
  selector: 'app-book',
  templateUrl: './book.page.html',
  styleUrls: ['./book.page.scss'],
})
export class BookPage implements OnInit {

  isbn: string;
  book: Book;

  constructor(private activatedRoute: ActivatedRoute,
              private router: Router,
              private auth: AuthService,
              private bookService: BookService) {

    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }

    this.isbn = this.activatedRoute.snapshot.params.isbn;

    // eslint-disable-next-line max-len
    /*this.book = new Book(isbn, 'Tiziano Sclavi', 'Nero', 'libro', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      new Date(), 125
    );*/
  }

  ngOnInit() {
    this.bookService.showBook(this.isbn).subscribe(
      data => this.book = data,
      error => console.log(error)
    );
  }

  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigate(['/login']),
      error => console.log(error)
    );
  }
}

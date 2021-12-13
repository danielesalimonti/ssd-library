import {Component, OnInit} from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {BookService} from '../../services/book.service';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  loadingBooks = true;
  loadingMyBooks = true;
  books: Book[] = [];
  isMyBook: string[] = [];

  constructor(private router: Router,
              private bookService: BookService,
              private auth: AuthService) {
    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.bookService.getAllBooks().subscribe(
      (data) => {
        this.books = data;
        this.loadingBooks = false;

        this.updateButtons();
      },
      error => {
        console.log(error);
        if(error.status === 403) {
          this.router.navigate(['/login']);
        }else{
          //router.navigate(['/error-page', error]);
        }
      });
  }

  updateButtons(){
    this.bookService.getMyBooks().subscribe(
      (myBooks) => {
        this.isMyBook = [];
        myBooks.forEach( (b) => {
          this.isMyBook.push(b.ISBN);
        });
        this.loadingMyBooks = false;
      },
      error => {
        console.log('error'+error);
        //router.navigate(['/error-page', error]);
      });
  }

  rent(isbn){
    this.bookService.rentBook(isbn).subscribe(
      data => {
        this.isMyBook.push(isbn);
        this.router.navigate(['/book/',isbn]);
        },
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

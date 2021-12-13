import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';

@Component({
  selector: 'app-my-books',
  templateUrl: './my-books.page.html',
  styleUrls: ['./my-books.page.scss'],
})
export class MyBooksPage implements OnInit {

  loadingBooks = true;
  myBooks: Book[] = [];

  constructor(private router: Router,
              private bookService: BookService,
              private auth: AuthService) {
    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.bookService.getMyBooks().subscribe(
      (data) => {
        this.myBooks = data;
        this.loadingBooks = false;
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


  logout(){
    this.auth.logout().subscribe(
      data =>{
        this.router.navigate(['/login']);
      },
      error => {
        console.log(error);
      }
    );
  }
}

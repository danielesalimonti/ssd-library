import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';
import {AlertController, ToastController} from "@ionic/angular";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-my-books',
  templateUrl: './my-books.page.html',
  styleUrls: ['./my-books.page.scss'],
})
export class MyBooksPage implements OnInit {

  loadingBooks = true;
  myBooks: Book[] = [];
  searchField: FormControl = new FormControl('');
  orderField: FormControl = new FormControl('');
  orderAscending = true;

  constructor(public router: Router,
              private bookService: BookService,
              private auth: AuthService,
              private toastController: ToastController) {

    if(!this.auth.isLogged()) {
      this.router.navigateByUrl('/login', {replaceUrl: true});
    }
  }

  ngOnInit() {
    this.bookService.getMyBooks().subscribe(
      (data) => {
        this.myBooks = data;
        this.loadingBooks = false;
      },
      error => {
        if(error.status === 0){
          error.error.detail = 'Lost Connection';
        }
        localStorage.setItem('error', JSON.stringify({status: error.status, message: error.error.detail}));
        this.router.navigateByUrl('/login', {replaceUrl: true});
      });
  }


  filter(books: Book[]): Book[]{
    return books.filter(b => this.searchField.value === ''
      || b.ISBN.includes(this.searchField.value)
      || b.title.toLowerCase().includes(this.searchField.value.toLowerCase())
      || b.author.toLowerCase().includes(this.searchField.value.toLowerCase()));
  }

  sort(books: Book[]): Book[]{
    return books.sort( (a, b) => {
      let c;
      switch(this.orderField.value){
        case 'ISBN': c = a.ISBN.localeCompare(b.ISBN); break;
        case 'Title': c = a.title.localeCompare(b.title); break;
        case 'Author': c = a.author.localeCompare(b.author); break;
        case 'PublishDate': c = a.published_date > b.published_date ? 1 : -1; break;
        default: return this.orderAscending ? 0 : -1;
      }
      return this.orderAscending ? c : -c;
    });
  }

  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigateByUrl('/login', {replaceUrl: true}),
      error => this.createToast(error)
    );
  }


  async createToast(error){
    if(error.status === 0){
      error.error.detail = 'Lost Connection';
    }

    const toast = await this.toastController.create({
      header: 'Error ',
      message: error.error.detail,
      position: 'top',
      duration: 5000,
      buttons:[
        {
          text: 'X',
          role: 'cancel'
        }
      ]
    });
    await toast.present();
  }
}

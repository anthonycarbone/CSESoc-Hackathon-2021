import React from 'react';
import algoliasearch from 'algoliasearch/lite';
import {
  InstantSearch,
  Hits,
  SearchBox,
  Pagination,
  Highlight,
  RefinementList,
} from 'react-instantsearch-dom';
import PropTypes from 'prop-types';
import './App.css';
import Subscribe from './Subscribe';

const searchClient = algoliasearch(
  'U5XKVGUK9E',
  '9c654c0f10a77436696ac45c08e4269d'
);

function App() {
  return (
    <div>
      <header className="header">
        <h1 className="header-title">
          <a href="/">Schollars</a>
        </h1>
        <div>
          {/* <Subscribe /> */}
        </div>
      </header>

      <div className="container">
        <InstantSearch searchClient={searchClient} indexName="schollars">
          <div className="search-panel">
          <div className="search-panel__filters">
              <RefinementList attribute="benefactor" />
            </div>
            <div className="search-panel__results">
              <SearchBox
                className="searchbox"
                translations={{
                  placeholder: 'Search scholarships...',
                }}
              />
              <Hits hitComponent={Hit} />

              <div className="pagination">
                <Pagination />
              </div>
            </div>
          </div>
        </InstantSearch>
      </div>
    </div>
  );
}

function Hit(props) {
  return (
    <article>
      <h1>
        <Highlight attribute="title" hit={props.hit} />
      </h1>
      <p>
        <Highlight attribute="notes" hit={props.hit} />
      </p>
    </article>
  );
}

Hit.propTypes = {
  hit: PropTypes.object.isRequired,
};

export default App;

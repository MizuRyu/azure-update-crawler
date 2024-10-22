import logging

from bs4 import BeautifulSoup

from parsers.base_parser import BaseParser

class AzureUpdatesParser(BaseParser):
    def parse(self, html):
        logging.debug('=== # start 記事(Azure Updates)のパース ===')
        soup = BeautifulSoup(html, 'html.parser')
        articles = []

        # 各記事のコンテナを取得
        containers = soup.find_all('div', class_='row')

        for container in containers:
            try:
                # 日付
                date_tag = container.find('p')
                date = date_tag.get_text(strip=True) if date_tag else ''

                # タイトルと詳細URL
                title_tag = container.find('h3').find('a')
                title = title_tag.get_text(strip=True) if title_tag else ''
                article_rul = title_tag['href'] if title_tag else ''

                # ステータス(PuPr, PrPr, GA等)
                release_status_tag = container.find_all('p')
                status = release_status_tag[1].get_text(strip=True) if len(release_status_tag) > 1 else ''

                # 詳細
                description = release_status_tag[2].get_text(strip=True) if len(release_status_tag) > 2 else ''

                article = {
                    'date': date,
                    'title': title,
                    'url': article_rul,
                    'status': status,
                    'description': description
                }

                articles.append(article)
            except Exception as e:
                logging.error('記事(Azure Updates)のパースに失敗しました。')
                logging.error(e)
                continue
        
        logging.debug(f'パースした記事数: {len(articles)}')
        logging.debug(f"パースした記事内容: {articles[0] if articles else 'なし'}")
        return articles

#######
# HTML要素の構造
# 以下が、1記事に対する構造となります。
#
# <div class="layout-container responsivegrid aem-GridColumn aem-GridColumn--default--12" data-component-id="121fbc03d93d1b908713185d26cbe5b5">
#     <div id="layout-container-uidd3db" data-componentname="layout-container-uidd3db" class="default" data-automation-test-id="picture-layout-container-uidd3db">
#         <div class="container">
#             <div class="row depth-0 default row-bg-color-layout-container-uidd3db" data-automation-test-id="mainContainer-layout-container-uidd3db">
#                 <style data-automation-test-id="bgcolorPicker-layout-container-uidd3db">
#                     .row-bg-color-layout-container-uidd3db {
#                         background-color: !important;
#                     }
#                 </style>
#                 <div class="col text-md-left no-gutters col-12 col-sm col-md-3" data-automation-test-id="column-layout-container-uidd3db">
#                     <div class="areaheading aem-GridColumn aem-GridColumn--default--12" data-component-id="54a8759731545a237e6d9c861d7dd0a3" oc-component-name="areaheading">
#                         <div class="area-heading" data-oc="oc925a" id="areaheading-oc925a">
#                             <div class="row">
#                                 <div class="col-12 col-md-8"></div>
#                                 <div class="col-12 col-md-8 col-xl-6">
#                                     <div data-oc-token-text="">
#                                         <p>Oct 10</p>
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#                 <div class="col text-md-left no-gutters col-12 col-md-9" data-automation-test-id="column-layout-container-uidd3db">
#                     <div class="richtext aem-GridColumn aem-GridColumn--default--12" data-component-id="9b992e252846bf14b532f40bd58c2fbe" oc-component-name="richtext">
#                         <section data-oc="occcb7" id="richtext-occcb7">
#                             <div data-oc-token-text="">
#                                 <h3>
#                                     <a href="https://azure.microsoft.com/en-us/updates/v2/End-of-Support-Announcement-for-Azure-Load-Balancer-numberOfProbes-property-on-1-September-2027" class="ms-rte-link">
#                                         <span style="font-weight: normal;">Retirement: End of Support Announcement for </span>Azure Load Balancer numberOfProbes property on September 1, 2027<span style="font-weight: normal;">.</span>
#                                     </a>
#                                 </h3>
#                             </div>
#                         </section>
#                     </div>
#                     <div class="richtext aem-GridColumn aem-GridColumn--default--12" data-component-id="9b992e252846bf14b532f40bd58c2fbe" oc-component-name="richtext">
#                         <section data-oc="oc8284" id="richtext-oc8284">
#                             <div data-oc-token-text="">
#                                 <p>RETIREMENT</p>
#                             </div>
#                         </section>
#                     </div>
#                     <div class="richtext aem-GridColumn aem-GridColumn--default--12" data-component-id="9b992e252846bf14b532f40bd58c2fbe" oc-component-name="richtext">
#                         <section data-oc="oc7ca0" id="richtext-oc7ca0">
#                             <div data-oc-token-text="">
#                                 <p>Support for Azure Load Balancer numberOfProbes property is ending</p>
#                             </div>
#                         </section>
#                     </div>
#                     <div class="link-list tabs aem-GridColumn aem-GridColumn--default--12" data-component-id="aede60019df22ec2319ebc487c7d75a1" oc-component-name="link-list">
#                         <section data-oc="oca998" id="link-list-oca998">
#                             <nav aria-label="Categories" _mstaria-label="156923">
#                                 <ul class="text-center d-flex flex-wrap list-inline small">
#                                     <li class="font-weight-semibold mx-1 my-2">
#                                         <section data-oc="oc54a0" id="badge-oc54a0">
#                                             <div class="mb-0">
#                                                 <span class="badge text-break-keep-all bg-gray-200 font-weight-light"> Retirements </span>
#                                             </div>
#                                         </section>
#                                     </li>
#                                 </ul>
#                             </nav>
#                         </section>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </div>
# </div>

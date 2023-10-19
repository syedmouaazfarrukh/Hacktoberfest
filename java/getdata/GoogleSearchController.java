import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
public class GoogleSearchController {

    @GetMapping("/google-search")
    public SearchResult googleSearch(@RequestParam String query) {
        if (query == null || query.isEmpty()) {
            return new SearchResult("Missing query parameter", null);
        }

        try {
            String searchUrl = "https://www.google.com/search?q=" + query;
            Document document = Jsoup.connect(searchUrl)
                                    .userAgent("Mozilla/5.0")
                                    .get();

            Element resultDiv = document.selectFirst("div.tF2Cxc");

            if (resultDiv != null) {
                String title = resultDiv.select("h3").text();
                String link = resultDiv.select("a").attr("href");
                return new SearchResult(title, link);
            } else {
                return new SearchResult("No search results found", null);
            }
        } catch (IOException e) {
            e.printStackTrace();
            return new SearchResult("Failed to retrieve search results", null);
        }
    }

    static class SearchResult {
        private final String title;
        private final String link;

        public SearchResult(String title, String link) {
            this.title = title;
            this.link = link;
        }

        public String getTitle() {
            return title;
        }

        public String getLink() {
            return link;
        }
    }
}

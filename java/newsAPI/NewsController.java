import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/news")
public class NewsController {
    private final String WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php";
    private final RestTemplate restTemplate;

    @Autowired
    public NewsController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping
    public ResponseEntity<?> getNews() {
        try {
            String newsArticles = getRecentNews();
            return ResponseEntity.ok(newsArticles);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("Failed to fetch news articles from Wikipedia");
        }
    }

    private String getRecentNews() {
        String apiUrl = WIKIPEDIA_API_URL;
        String queryUrl = apiUrl + "?action=query&format=json&list=recentchanges&rcnamespace=0&rclimit=10&rcshow=!minor|!bot&rctype=edit|new";
        return restTemplate.getForObject(queryUrl, String.class);
    }
}

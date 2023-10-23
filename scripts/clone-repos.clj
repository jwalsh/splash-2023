;; Example code for cloning the repository and running the project
;; (defproject github-repo "splash-2023")
(def clones {:github-repo "https://github.com/jwalsh/splash-2023"})
(defn clone-repos [clones]
  (doseq [[name url] clones]
    (println "Cloning" name "from" url)
    (shell/sh "git" "clone" url (str name))))

(clone-repos clones)

(shell/sh "lein" "run" "-m" "splash-2023.core")

(ns my-app.core
  (:require [clj-icalendar.parse :as parse]
            [clojure.java.io :as io]))

(defn read-ics [path]
  (-> path
      io/resource
      slurp
      parse/ics->maps))

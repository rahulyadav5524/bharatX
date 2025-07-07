"use client"

import type React from "react"

import { useState } from "react"
import { Search, Clock, ExternalLink, Star } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface SearchResult {
  link: string
  price: string[]
  currency: string
  product_name: string
}



export default function SearchDashboard() {
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setIsSearching(true)
    setHasSearched(true)

  const data = await fetch("https://bharat-x-sepia.vercel.app/api/search/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: searchQuery }),
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error("Error fetching search results:", error)
        return []
      })


    setSearchResults(data?.data?.data || [])
    setIsSearching(false)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch()
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case "documentation":
        return "bg-blue-100 text-blue-800 hover:bg-blue-200"
      case "tutorial":
        return "bg-green-100 text-green-800 hover:bg-green-200"
      case "guide":
        return "bg-purple-100 text-purple-800 hover:bg-purple-200"
      default:
        return "bg-gray-100 text-gray-800 hover:bg-gray-200"
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Search Dashboard</h1>
          <p className="text-gray-600 text-lg">Find the information you need quickly and easily</p>
        </div>

        {/* Search Section */}
        <Card className="mb-8 shadow-lg">
          <CardContent className="p-6">
            <div className="flex gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Enter your search query..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="pl-10 h-12 text-lg"
                />
              </div>
              <Button
                onClick={handleSearch}
                disabled={isSearching || !searchQuery.trim()}
                className="h-12 px-8 text-lg"
              >
                {isSearching ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-4 w-4" />
                    Search
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        {hasSearched && (
          <div className="space-y-4">
            {/* Results Header */}
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-900">
                Search Results
                {!isSearching && (
                  <span className="text-gray-500 text-lg ml-2">
                    ({searchResults.length} {searchResults.length === 1 ? "result" : "results"} found)
                  </span>
                )}
              </h2>
            </div>

            {/* Loading State */}
            {isSearching && (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <Card key={i} className="animate-pulse">
                    <CardContent className="p-6">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-full mb-1"></div>
                      <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Results List */}
            { !isSearching && searchResults.length > 0 && (
              <div className="space-y-4">
                {searchResults.map((result, key) => (
                  <Card key={key} className="hover:shadow-lg transition-shadow duration-200">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="text-xl text-blue-600 hover:text-blue-800 flex items-center gap-2">
                            {result.product_name}
                          </CardTitle>
                          <div className="flex items-center gap-4 mt-2">
                            <Badge className={getCategoryColor(result.currency)}>{result.currency}</Badge>
                            <div className="flex items-center gap-1 text-sm text-gray-500">
                              <Clock className="h-3 w-3" />
                              <span>{result.link}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <CardDescription className="text-gray-600 leading-relaxed">
                        {result.prices.map((price, index) => (
                          <span key={index} className="block text-lg font-semibold text-gray-800">
                            {price}
                          </span>
                        ))}
                      </CardDescription>
                      <div className="mt-4">
                        <Button
                          variant="outline"
                          size="sm"
                          className="text-blue-600 hover:text-blue-800 bg-transparent"
                          onClick={() => window.open(result.link, "_blank")}
                        >
                          View Details
                          <ExternalLink className="ml-1 h-3 w-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* No Results */}
            {!isSearching && searchResults.length === 0 && (
              <Card className="text-center py-12">
                <CardContent>
                  <div className="text-gray-400 mb-4">
                    <Search className="h-16 w-16 mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-600 mb-2">No results found</h3>
                  <p className="text-gray-500">{"Try adjusting your search terms or check for typos."}</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {/* Initial State */}
        {!hasSearched && (
          <Card className="text-center py-16 bg-gradient-to-r from-blue-50 to-indigo-50">
            <CardContent>
              <div className="text-blue-400 mb-4">
                <Search className="h-20 w-20 mx-auto" />
              </div>
              <h3 className="text-2xl font-semibold text-gray-700 mb-2">Ready to search?</h3>
              <p className="text-gray-500 text-lg">Enter your search query above to find relevant results</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

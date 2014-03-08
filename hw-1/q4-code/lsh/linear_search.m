% 
% linear_search.m 
% 

function [idxs] = linear_search(patches, query_idx, k)
	d = sum(abs(bsxfun(@minus,patches(:, query_idx), patches)));
	[ignore, ind] = sort(d);
	idxs = ind(1:k); % I(1:k)
end

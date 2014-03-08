function [idxs] = plot10nn(patches)
	N = 10+1; % number of NNs 
	query_idx = 100; % query point 
	T = lsh('lsh', 10, 24, size(patches, 1), patches, 'range', 255);
	nnlsh = [];
	while length(nnlsh) < N
		[nnlsh, numcand] = lshlookup(patches(:, query_idx), patches, T, 'k', N, 'distfun', 'lpnorm', 'distargs', {1});
	end
	nnlin = linear_search(patches, query_idx, N);
	% plot, plot, ..., plot !!! :) 
	figure(1);
	clf;
	for k = 1:10
		subplot(2, 5, k);
		imagesc(reshape(patches(:, nnlsh(k+1)), 20, 20));
		colormap gray;
		axis image;
	end
	% and again 
	figure(2);
	clf;
	for k = 1:10
		subplot(2, 5, k);
		imagesc(reshape(patches(:, nnlin(k+1)), 20, 20));
		colormap gray;
		axis image;
	end
	% and, finally, point the query image 
	figure(3);
	clf;
	imagesc(reshape(patches(:, query_idx), 20, 20));
	colormap gray;
	axis image;
end
